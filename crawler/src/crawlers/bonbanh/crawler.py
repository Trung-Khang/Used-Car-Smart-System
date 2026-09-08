"""
Bonbanh Vehicle Crawler.
Responsible for HTTP session management, navigation, pagination,
collecting detail URLs, throttling, deduplication, retry, checkpointing, and output generation.
"""

import argparse
from datetime import datetime, timezone
import http.cookiejar
import json
import logging
import os
from pathlib import Path
import random
import sys
import time
from typing import Any, Dict, List, Optional, Set
import urllib.request

# Support both direct execution and package import
try:
    from crawler.src.crawlers.bonbanh.parser import (
        extract_listing_items,
        is_valid_detail_url,
        normalize_url,
        parse_detail_page,
    )
except (ImportError, ModuleNotFoundError):
    try:
        from .parser import (
            extract_listing_items,
            is_valid_detail_url,
            normalize_url,
            parse_detail_page,
        )
    except (ImportError, ModuleNotFoundError):
        from parser import (
            extract_listing_items,
            is_valid_detail_url,
            normalize_url,
            parse_detail_page,
        )

BASE_LISTING_URL = "https://bonbanh.com/oto"
REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_RAW_DIR = REPO_ROOT / "crawler" / "data" / "raw"
DEFAULT_TMP_DIR = REPO_ROOT / "crawler" / "data" / "tmp"
DEFAULT_LOG_DIR = REPO_ROOT / "crawler" / "logs"
CHECKPOINT_FILE = DEFAULT_TMP_DIR / "bonbanh_checkpoint.json"
LOG_FILE = DEFAULT_LOG_DIR / "bonbanh_crawler.log"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
}


def setup_logger(log_file: Path = LOG_FILE) -> logging.Logger:
    """Configure logger with console and file handlers."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("bonbanh_crawler")
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
                return json.load(f)
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


class BonbanhCrawler:
    """
    HTTP-session-based Bonbanh vehicle crawler.
    Uses resilient session management, rate limiting, and bounded retries.
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
            self.output_path = DEFAULT_RAW_DIR / f"bonbanh_raw_{ts}.json"

        self.checkpoint_mgr = CheckpointManager()
        self.processed_urls: Set[str] = set()
        self.start_page = 1

        # Build cookie opener
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        self.opener.addheaders = list(DEFAULT_HEADERS.items())

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

    def _fetch_html(self, url: str, max_retries: int = 3, timeout: int = 20) -> Optional[str]:
        """Fetch URL with bounded retries and exponential backoff."""
        for attempt in range(1, max_retries + 1):
            try:
                req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
                with self.opener.open(req, timeout=timeout) as resp:
                    if resp.status == 200:
                        return resp.read().decode("utf-8", errors="ignore")
                    else:
                        logger.warning(f"HTTP {resp.status} for {url}")
            except Exception as e:
                self.stats["network_failures"] += 1
                logger.warning(
                    f"Fetch attempt {attempt}/{max_retries} failed for {url}: {e}"
                )
                if attempt < max_retries:
                    backoff = attempt * 2.5
                    time.sleep(backoff)
        return None

    def run(self) -> List[Dict[str, Any]]:
        """Execute Bonbanh crawler run."""
        logger.info("=" * 60)
        logger.info("Bonbanh Crawler starting run")
        logger.info(
            f"Config: max_pages={self.max_pages}, limit={self.limit}, "
            f"resume={self.resume}, output={self.output_path}"
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
        current_page_num = self.start_page
        pages_crawled_count = 0

        while pages_crawled_count < self.max_pages and len(records) < self.limit:
            listing_url = (
                BASE_LISTING_URL
                if current_page_num == 1
                else f"{BASE_LISTING_URL}/page,{current_page_num}"
            )

            logger.info(f"Navigating to listing page {current_page_num}: {listing_url}")
            self.stats["pages_attempted"] += 1

            listing_html = self._fetch_html(listing_url)
            if not listing_html:
                logger.error(
                    f"Failed to load listing page {current_page_num}. Skipping to next page."
                )
                pages_crawled_count += 1
                current_page_num += 1
                time.sleep(3.0)
                continue

            items = extract_listing_items(listing_html)
            self.stats["urls_discovered"] += len(items)
            logger.info(
                f"Page {current_page_num}: discovered {len(items)} listing items"
            )

            if not items:
                logger.warning(
                    f"No detail URLs discovered on page {current_page_num}. Ending pagination."
                )
                break

            # Filter duplicates
            new_items = []
            for it in items:
                u = it["url"]
                if u in self.processed_urls:
                    self.stats["duplicate_urls_skipped"] += 1
                else:
                    new_items.append(it)

            logger.info(
                f"Page {current_page_num}: {len(new_items)} new URLs to process "
                f"({len(items) - len(new_items)} duplicates skipped)"
            )

            # Process detail pages
            for it in new_items:
                if len(records) >= self.limit:
                    logger.info(
                        f"Reached records limit ({self.limit}). Stopping detail collection."
                    )
                    break

                detail_url = it["url"]
                listing_loc = it["location"]

                logger.info(f"Processing detail [{len(records) + 1}/{self.limit}]: {detail_url}")
                self.stats["details_attempted"] += 1

                detail_html = self._fetch_html(detail_url, timeout=20)
                if not detail_html:
                    logger.warning(f"Could not load detail page: {detail_url}. Skipping.")
                    continue

                crawled_at = datetime.now(timezone.utc).isoformat()
                record = parse_detail_page(
                    detail_html,
                    detail_url,
                    listing_location=listing_loc,
                    crawled_at=crawled_at,
                )

                if record:
                    records.append(record)
                    self.processed_urls.add(detail_url)
                    self.stats["records_saved"] += 1
                    logger.info(
                        f"Successfully parsed: {record.get('brand')} {record.get('model')} "
                        f"({record.get('manufacture_year')}) - Price: {record.get('price')} VND"
                    )
                else:
                    self.stats["parse_failures"] += 1
                    logger.warning(
                        f"Detail page at {detail_url} produced no valid record. Skipped."
                    )

                # Throttling delay between detail requests (1.0 to 1.8 seconds)
                time.sleep(random.uniform(1.0, 1.8))

            # Save checkpoint and flush output after page completes
            self.stats["pages_succeeded"] += 1
            self.checkpoint_mgr.save(current_page_num, self.processed_urls)
            self._save_output(records)

            pages_crawled_count += 1
            current_page_num += 1

            # Pause between listing pages
            if pages_crawled_count < self.max_pages and len(records) < self.limit:
                time.sleep(random.uniform(2.0, 3.5))

        # Final save output
        self._save_output(records)

        logger.info("=" * 60)
        logger.info("Bonbanh Crawler finished.")
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
    parser = argparse.ArgumentParser(description="Bonbanh Used Car Python Crawler")
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
        help="Run browser in headless mode (default: True, compatibility flag)",
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
        help="Browser channel (compatibility flag)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    crawler = BonbanhCrawler(
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
