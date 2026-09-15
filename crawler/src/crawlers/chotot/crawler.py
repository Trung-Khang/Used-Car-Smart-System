"""
Chợ Tốt Vehicle Crawler.
Responsible for browser lifecycle, navigation, pagination, controlled scrolling,
collecting URLs, throttling, deduplication, retry, checkpointing, and output generation.
"""

import argparse
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import random
import sys
import time
from typing import Any, Dict, List, Optional, Set

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

# Support both direct script execution and package import
try:
    from crawler.src.crawlers.chotot.parser import (
        extract_listing_urls,
        is_valid_detail_url,
        normalize_url,
        parse_detail_page,
    )
except (ImportError, ModuleNotFoundError):
    try:
        from .parser import (
            extract_listing_urls,
            is_valid_detail_url,
            normalize_url,
            parse_detail_page,
        )
    except (ImportError, ModuleNotFoundError):
        from parser import (
            extract_listing_urls,
            is_valid_detail_url,
            normalize_url,
            parse_detail_page,
        )

BASE_LISTING_URL = "https://xe.chotot.com/mua-ban-oto"
REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_RAW_DIR = REPO_ROOT / "crawler" / "data" / "raw"
DEFAULT_TMP_DIR = REPO_ROOT / "crawler" / "data" / "tmp"
DEFAULT_LOG_DIR = REPO_ROOT / "crawler" / "logs"
CHECKPOINT_FILE = DEFAULT_TMP_DIR / "chotot_checkpoint.json"
LOG_FILE = DEFAULT_LOG_DIR / "chotot_crawler.log"


def setup_logger(log_file: Path = LOG_FILE) -> logging.Logger:
    """Configure logger with console and file handlers."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("chotot_crawler")
    logger.setLevel(logging.INFO)

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
        except Exception:
            pass

    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File handler (UTF-8)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


logger = setup_logger()


class CheckpointManager:
    """Manages crawl checkpoint state inside crawler/data/tmp/."""

    def __init__(self, filepath: Path = CHECKPOINT_FILE):
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        if not self.filepath.exists():
            return {
                "last_successful_page": 0,
                "processed_urls": [],
                "updated_at": None,
            }
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            logger.warning(f"Could not read checkpoint from {self.filepath}: {e}")
            return {
                "last_successful_page": 0,
                "processed_urls": [],
                "updated_at": None,
            }

    def save(self, last_page: int, processed_urls: Set[str]) -> None:
        try:
            data = {
                "last_successful_page": last_page,
                "processed_urls": list(processed_urls),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(
                f"Checkpoint saved: last_page={last_page}, total_processed_urls={len(processed_urls)}"
            )
        except Exception as e:
            logger.error(f"Failed to save checkpoint to {self.filepath}: {e}")


class ChototCrawler:
    """
    Playwright-based Chợ Tốt vehicle crawler.
    """

    def __init__(
        self,
        max_pages: int = 1,
        limit: int = 5,
        headless: bool = True,
        resume: bool = False,
        output_file: Optional[str] = None,
        browser_channel: Optional[str] = None,
    ):
        self.max_pages = max_pages
        self.limit = limit
        self.headless = headless
        self.resume = resume
        self.browser_channel = browser_channel

        # Establish output path
        DEFAULT_RAW_DIR.mkdir(parents=True, exist_ok=True)
        if output_file:
            self.output_path = Path(output_file)
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_path = DEFAULT_RAW_DIR / f"chotot_raw_{ts}.json"

        self.checkpoint_mgr = CheckpointManager()
        self.processed_urls: Set[str] = set()
        self.start_page = 1

        # Statistics
        self.stats = {
            "pages_attempted": 0,
            "pages_succeeded": 0,
            "urls_discovered": 0,
            "duplicate_urls_skipped": 0,
            "details_attempted": 0,
            "records_saved": 0,
            "parse_failures": 0,
            "network_failures": 0,
        }

    def _init_browser(self, p: Any) -> Browser:
        """Launch browser with robust channel fallback (msedge -> chrome -> chromium)."""
        channels_to_try = []
        if self.browser_channel:
            channels_to_try = [self.browser_channel]
        else:
            channels_to_try = ["msedge", "chrome", None]

        last_err = None
        for ch in channels_to_try:
            try:
                if ch:
                    browser = p.chromium.launch(channel=ch, headless=self.headless)
                    logger.info(f"Browser launched successfully using channel: {ch}")
                else:
                    browser = p.chromium.launch(headless=self.headless)
                    logger.info("Browser launched successfully using default chromium")
                return browser
            except Exception as e:
                last_err = e
                logger.warning(f"Failed to launch browser with channel {ch}: {e}")

        raise RuntimeError(f"Could not launch any browser. Last error: {last_err}")

    def _scroll_listing_page(self, page: Page, max_scrolls: int = 3) -> None:
        """Perform controlled scrolling to trigger lazy-loaded listings."""
        for i in range(max_scrolls):
            try:
                page.evaluate("window.scrollBy(0, window.innerHeight)")
                time.sleep(1.2)
            except Exception as e:
                logger.warning(f"Scroll step {i+1} encountered error: {e}")
                break

    def _navigate_with_retry(
        self, page: Page, url: str, max_retries: int = 3, timeout: int = 30000
    ) -> bool:
        """Navigate to URL with bounded retries and exponential backoff."""
        for attempt in range(1, max_retries + 1):
            try:
                page.goto(url, timeout=timeout, wait_until="domcontentloaded")
                time.sleep(1.0)
                return True
            except Exception as e:
                self.stats["network_failures"] += 1
                logger.warning(
                    f"Navigation attempt {attempt}/{max_retries} failed for {url}: {e}"
                )
                if attempt < max_retries:
                    backoff = attempt * 2.5
                    time.sleep(backoff)
        return False

    def _new_context_and_page(self, browser: Browser):
        """Create a new browser context and page with media abort route to maximize speed and stability."""
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        def block_media(route):
            if route.request.resource_type in ["image", "media", "font"]:
                route.abort()
            else:
                route.continue_()

        page.route("**/*", block_media)
        return context, page

    def run(self) -> List[Dict[str, Any]]:
        """Execute crawler run."""
        logger.info("=" * 60)
        logger.info("Chợ Tốt Crawler starting run")
        logger.info(
            f"Config: max_pages={self.max_pages}, limit={self.limit}, "
            f"headless={self.headless}, resume={self.resume}, output={self.output_path}"
        )

        if self.resume:
            chk = self.checkpoint_mgr.load()
            last_page = chk.get("last_successful_page", 0)
            self.start_page = last_page + 1
            self.processed_urls = set(chk.get("processed_urls", []))
            logger.info(
                f"Resuming from checkpoint: starting at page {self.start_page}, "
                f"loaded {len(self.processed_urls)} already processed URLs"
            )
        else:
            self.start_page = 1
            self.processed_urls = set()

        records: List[Dict[str, Any]] = []
        items_since_recycle = 0
        RECYCLE_INTERVAL = 25

        with sync_playwright() as p:
            browser = self._init_browser(p)
            context, page = self._new_context_and_page(browser)

            current_page_num = self.start_page
            pages_crawled_count = 0

            try:
                while pages_crawled_count < self.max_pages and len(records) < self.limit:
                    listing_url = (
                        BASE_LISTING_URL
                        if current_page_num == 1
                        else f"{BASE_LISTING_URL}?page={current_page_num}"
                    )

                    logger.info(f"Navigating to listing page {current_page_num}: {listing_url}")
                    self.stats["pages_attempted"] += 1

                    success = self._navigate_with_retry(page, listing_url)
                    if not success:
                        logger.error(
                            f"Failed to load listing page {current_page_num}. Skipping to next page."
                        )
                        pages_crawled_count += 1
                        current_page_num += 1
                        time.sleep(3.0)
                        continue

                    # Controlled scroll for lazy load
                    self._scroll_listing_page(page, max_scrolls=3)

                    # Extract URLs
                    listing_html = page.content()
                    discovered_urls = extract_listing_urls(listing_html)
                    self.stats["urls_discovered"] += len(discovered_urls)
                    logger.info(
                        f"Page {current_page_num}: discovered {len(discovered_urls)} listing URLs"
                    )

                    if not discovered_urls:
                        logger.warning(
                            f"No detail URLs discovered on page {current_page_num}. Ending pagination."
                        )
                        break

                    # Filter new URLs
                    new_urls: List[str] = []
                    for u in discovered_urls:
                        if u in self.processed_urls:
                            self.stats["duplicate_urls_skipped"] += 1
                        else:
                            new_urls.append(u)

                    logger.info(
                        f"Page {current_page_num}: {len(new_urls)} new URLs to process "
                        f"({len(discovered_urls) - len(new_urls)} duplicates skipped)"
                    )

                    # Process detail pages
                    page_detail_success = True
                    for detail_url in new_urls:
                        if len(records) >= self.limit:
                            logger.info(
                                f"Reached records limit ({self.limit}). Stopping detail collection."
                            )
                            break

                        logger.info(f"Processing detail [{len(records) + 1}/{self.limit}]: {detail_url}")
                        self.stats["details_attempted"] += 1

                        detail_ok = self._navigate_with_retry(page, detail_url, timeout=25000)
                        if not detail_ok:
                            logger.warning(f"Could not load detail page: {detail_url}. Skipping.")
                            continue

                        detail_html = page.content()
                        crawled_at = datetime.now(timezone.utc).isoformat()
                        record = parse_detail_page(detail_html, detail_url, crawled_at=crawled_at)

                        if record:
                            records.append(record)
                            self.processed_urls.add(detail_url)
                            self.stats["records_saved"] += 1
                            logger.info(
                                f"Successfully parsed: {record.get('brand')} {record.get('model')} "
                                f"({record.get('manufacture_year')}) - Price: {record.get('price')}"
                            )
                        else:
                            self.stats["parse_failures"] += 1
                            logger.warning(
                                f"Detail page at {detail_url} produced no valid record. Skipped."
                            )

                        # Throttling delay between detail requests (1.0 to 1.8 seconds)
                        time.sleep(random.uniform(1.0, 1.8))

                        items_since_recycle += 1
                        if items_since_recycle >= RECYCLE_INTERVAL:
                            logger.info(
                                f"Recycling browser context after {items_since_recycle} items to preserve performance & stability..."
                            )
                            try:
                                page.close()
                                context.close()
                            except Exception:
                                pass
                            time.sleep(1.5)
                            context, page = self._new_context_and_page(browser)
                            items_since_recycle = 0

                    # Save checkpoint and flush output after page completes
                    self.stats["pages_succeeded"] += 1
                    self.checkpoint_mgr.save(current_page_num, self.processed_urls)
                    self._save_output(records)

                    pages_crawled_count += 1
                    current_page_num += 1

                    # Short pause between listing pages
                    if pages_crawled_count < self.max_pages and len(records) < self.limit:
                        time.sleep(random.uniform(2.0, 3.5))

            finally:
                self._save_output(records)
                context.close()
                browser.close()

            # Write final output
            self._save_output(records)

            logger.info("=" * 60)
            logger.info("Chợ Tốt Crawler finished.")
            logger.info(f"Summary: {json.dumps(self.stats, indent=2)}")
            logger.info(f"Output saved to: {self.output_path} ({len(records)} records)")
            return records

    def _save_output(self, records: List[Dict[str, Any]]) -> None:
        """Save emitted records into raw JSON format."""
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(records)} records to {self.output_path}")
        except Exception as e:
            logger.error(f"Failed to write output to {self.output_path}: {e}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chợ Tốt Used Car Python Crawler")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=1,
        help="Maximum listing pages to scrape (default: 1)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum vehicle records to extract (default: 5)",
    )
    parser.add_argument(
        "--headless",
        type=lambda v: v.lower() in ["true", "1", "yes"],
        default=True,
        help="Run browser in headless mode (default: True)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=False,
        help="Resume crawling from checkpoint",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output file path for raw JSON",
    )
    parser.add_argument(
        "--browser-channel",
        type=str,
        default=None,
        help="Browser channel to use ('msedge', 'chrome', or omit for auto)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    crawler = ChototCrawler(
        max_pages=args.max_pages,
        limit=args.limit,
        headless=args.headless,
        resume=args.resume,
        output_file=args.output,
        browser_channel=args.browser_channel,
    )
    crawler.run()


if __name__ == "__main__":
    main()
