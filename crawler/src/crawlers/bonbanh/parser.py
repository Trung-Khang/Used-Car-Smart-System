"""
Bonbanh HTML Parser module.
Responsible for extracting listing URLs and parsing detail page data
strictly into the 14-field project data contract.
"""

from datetime import datetime, timezone
import re
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup

BASE_URL = "https://bonbanh.com"
DETAIL_URL_PATTERN = re.compile(r"xe-.*-\d+$", re.IGNORECASE)
YEAR_PATTERN = re.compile(r"\b(19\d{2}|20\d{2})\b")

MULTI_WORD_BRANDS = [
    "mercedes-benz",
    "mercedes benz",
    "land rover",
    "aston martin",
    "rolls-royce",
    "rolls royce",
    "alfa romeo",
]


def normalize_url(url: str, base: str = BASE_URL) -> str:
    """Normalize Bonbanh detail URL by removing fragments and query params."""
    if not url:
        return ""
    full_url = urljoin(base, url.strip().lstrip("/"))
    parsed = urlparse(full_url)
    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
    return clean_url


def is_valid_detail_url(url: str) -> bool:
    """Check if URL matches a valid Bonbanh vehicle detail URL pattern."""
    if not url:
        return False
    clean = url.split("?")[0].split("#")[0].rstrip("/")
    return bool(DETAIL_URL_PATTERN.search(clean))


def parse_price(price_str: Optional[str]) -> Optional[int]:
    """
    Parse Vietnamese price string into integer VND amount.
    Examples:
        '406 Triệu' -> 406000000
        '1 Tỷ 667 Triệu' -> 1667000000
        '1,25 Tỷ' -> 1250000000
        '555 Tr' -> 555000000
        '40000000' -> 40000000
    """
    if not price_str:
        return None
    s = price_str.strip().replace(",", ".")

    ty_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:tỷ|ti|ty)", s, re.IGNORECASE)
    trieu_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:triệu|trieu|tr)", s, re.IGNORECASE)

    total = 0.0
    found = False
    if ty_match:
        try:
            total += float(ty_match.group(1)) * 1_000_000_000
            found = True
        except ValueError:
            pass
    if trieu_match:
        try:
            total += float(trieu_match.group(1)) * 1_000_000
            found = True
        except ValueError:
            pass

    if found and total > 0:
        return int(round(total))

    # Check for direct integer amount
    digits = re.sub(r"[^\d]", "", s)
    if digits and len(digits) >= 7:  # At least 1 million VND
        try:
            return int(digits)
        except ValueError:
            pass

    return None


def split_brand_model(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Split combined brand and model string.
    Handles known multi-word brands (Mercedes Benz, Land Rover, etc.).
    """
    if not text:
        return None, None
    t = text.strip()
    tl = t.lower()
    for b in MULTI_WORD_BRANDS:
        if tl.startswith(b):
            brand = t[: len(b)].strip()
            model = t[len(b) :].strip()
            return brand, model if model else None

    parts = t.split(" ", 1)
    brand = parts[0].strip()
    model = parts[1].strip() if len(parts) > 1 else None
    return brand, model


def extract_listing_items(
    html: str, base_url: str = BASE_URL
) -> List[Dict[str, Optional[str]]]:
    """
    Extract listing items from Bonbanh listing page HTML.
    Returns list of dicts with normalized 'url' and listing 'location'.
    """
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    items: List[Dict[str, Optional[str]]] = []
    seen: set = set()

    car_nodes = soup.select(".car-item")
    if car_nodes:
        for node in car_nodes:
            a_tag = node.find("a", href=True)
            if not a_tag:
                continue
            href = a_tag["href"].strip()
            norm_url = normalize_url(href, base=base_url)
            if not is_valid_detail_url(norm_url) or norm_url in seen:
                continue
            seen.add(norm_url)

            # Location from .cb4
            cb4 = node.select_one(".cb4")
            loc_val = None
            if cb4:
                raw_loc = cb4.get_text(strip=True)
                loc_val = re.sub(r"(?i)^nơi bán:\s*", "", raw_loc).strip()
                if not loc_val or loc_val.lower() == "chưa rõ":
                    loc_val = None

            items.append({"url": norm_url, "location": loc_val})
    else:
        # Fallback: scan all a tags
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            norm_url = normalize_url(href, base=base_url)
            if is_valid_detail_url(norm_url) and norm_url not in seen:
                seen.add(norm_url)
                items.append({"url": norm_url, "location": None})

    return items


def _extract_specs(soup: BeautifulSoup) -> Dict[str, str]:
    """Extract key-value pairs from detail specification rows."""
    specs: Dict[str, str] = {}
    for lbl_div in soup.find_all("div", class_="label"):
        lbl_text = lbl_div.get_text(strip=True).rstrip(":")
        parent = lbl_div.parent
        if parent:
            val_elem = parent.find("div", class_="txt_input") or parent.find(
                "span", class_="inp"
            )
            if val_elem:
                val_text = val_elem.get_text(strip=True)
                if lbl_text and val_text:
                    specs[lbl_text] = val_text
    return specs


def _extract_detail_location(soup: BeautifulSoup) -> Optional[str]:
    """Extract location from seller contact information."""
    for box in soup.select(".contact-box, .contact_box, #contact, #mail_parent"):
        text = box.get_text(" ", strip=True)
        m = re.search(r"Địa chỉ:\s*([^,\n\r]+(?:,[^,\n\r]+)*)", text, re.IGNORECASE)
        if m:
            loc = m.group(1).strip()
            if loc:
                return loc

    # Check seller address span or div
    elem = soup.find(string=re.compile(r"Địa chỉ:", re.IGNORECASE))
    if elem:
        p = elem.find_parent()
        if p:
            txt = p.get_text(strip=True)
            txt = re.sub(r"(?i)^địa chỉ:\s*", "", txt).strip()
            if txt:
                return txt

    return None


def _extract_listed_at(soup: BeautifulSoup, html: str) -> Optional[str]:
    """Extract listing date from Bonbanh detail page."""
    # Pattern: 'Đăng ngày 7/09/2026'
    m = re.search(r"Đăng ngày\s*([\d/]+)", html, re.IGNORECASE)
    if m:
        return m.group(1).strip()

    elem = soup.find(string=re.compile(r"Đăng ngày", re.IGNORECASE))
    if elem:
        m2 = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", str(elem))
        if m2:
            return m2.group(1).strip()

    return None


def _extract_image_url(soup: BeautifulSoup) -> Optional[str]:
    """Extract primary vehicle image URL."""
    # From meta og:image
    meta_img = soup.find("meta", attrs={"property": "og:image"})
    if meta_img and meta_img.get("content"):
        content = meta_img["content"].strip()
        if content and not content.endswith("logo.png"):
            return content

    # From main gallery image
    large_img = soup.select_one("#large_img img, .car-image img, #gallery img")
    if large_img and large_img.get("src"):
        src = large_img["src"].strip()
        if src and not src.endswith("logo.png"):
            return urljoin(BASE_URL, src)

    return None


def parse_detail_page(
    html: str,
    source_url: str,
    listing_location: Optional[str] = None,
    crawled_at: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Parse a Bonbanh vehicle detail page HTML into the authoritative 14-field record.
    Returns None if the page is invalid or missing required identifiers.
    """
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    specs = _extract_specs(soup)

    # 1. H1 parsing for Brand, Model, Variant, Year, Price
    h1 = soup.find("h1")
    brand = None
    model = None
    variant = None
    year_from_h1 = None
    price_from_h1 = None

    if h1:
        raw_h1 = h1.get_text()
        if "-" in raw_h1:
            left_part, price_part = raw_h1.rsplit("-", 1)
            price_from_h1 = price_part.strip()
        else:
            left_part = raw_h1

        lines = [line.strip() for line in left_part.splitlines() if line.strip()]
        if lines and lines[0].lower() == "xe":
            lines = lines[1:]

        if lines:
            brand_model_text = lines[0]
            brand, model = split_brand_model(brand_model_text)

        if len(lines) >= 2:
            second_line = lines[1]
            # Check if second line is a 4-digit year
            if YEAR_PATTERN.fullmatch(second_line):
                year_from_h1 = int(second_line)
            else:
                variant = second_line

        if len(lines) >= 3:
            third_line = lines[2]
            if YEAR_PATTERN.fullmatch(third_line):
                year_from_h1 = int(third_line)
            elif not variant:
                variant = third_line

    # Fallback from URL slug if brand or model missing
    if not brand or not model:
        # e.g. https://bonbanh.com/xe-mercedes_benz-c_class-c250-amg-2015-6969599
        slug = source_url.split("/")[-1].replace("xe-", "")
        slug_parts = slug.split("-")
        if slug_parts and not brand:
            brand = slug_parts[0].replace("_", " ").title()
        if len(slug_parts) > 1 and not model:
            model = slug_parts[1].replace("_", " ").title()

    # 4. manufacture_year
    manufacture_year = None
    spec_year = specs.get("Năm sản xuất")
    if spec_year:
        m_yr = YEAR_PATTERN.search(spec_year)
        if m_yr:
            try:
                manufacture_year = int(m_yr.group(1))
            except ValueError:
                pass
    if not manufacture_year and year_from_h1:
        manufacture_year = year_from_h1
    if not manufacture_year:
        m_slug_yr = YEAR_PATTERN.search(source_url)
        if m_slug_yr:
            try:
                manufacture_year = int(m_slug_yr.group(1))
            except ValueError:
                pass

    # 5. price (numeric VND)
    price = None
    if price_from_h1:
        price = parse_price(price_from_h1)
    if price is None:
        price_tag = soup.select_one(".price, .car_price, .gia_xe, .tag_price")
        if price_tag:
            price = parse_price(price_tag.get_text(strip=True))

    # 6. mileage
    mileage = None
    km_spec = specs.get("Số Km đã đi")
    if km_spec:
        mileage = km_spec.strip()

    # 7. fuel_type
    fuel_type = None
    engine_spec = specs.get("Động cơ", "")
    fuel_spec = specs.get("Nhiên liệu", "")
    combined_fuel_text = f"{engine_spec} {fuel_spec}".strip()

    if re.search(r"xăng", combined_fuel_text, re.IGNORECASE):
        fuel_type = "Xăng"
    elif re.search(r"dầu|diesel", combined_fuel_text, re.IGNORECASE):
        fuel_type = "Dầu"
    elif re.search(r"hybrid|lai", combined_fuel_text, re.IGNORECASE):
        fuel_type = "Hybrid"
    elif re.search(r"điện|electric", combined_fuel_text, re.IGNORECASE):
        fuel_type = "Điện"
    elif combined_fuel_text:
        fuel_type = combined_fuel_text

    # 8. transmission
    transmission = specs.get("Hộp số")

    # 9. body_type
    body_type = specs.get("Kiểu dáng")

    # 10. location
    location = listing_location or _extract_detail_location(soup)

    # 11. source_url
    clean_source_url = normalize_url(source_url)

    # 12. image_url
    image_url = _extract_image_url(soup)

    # 13. listed_at
    listed_at = _extract_listed_at(soup, html)

    # 14. crawled_at
    if not crawled_at:
        crawled_at = datetime.now(timezone.utc).isoformat()

    # Basic validity validation
    if not clean_source_url or (not brand and not model and not price):
        return None

    def _c(s: Any) -> Optional[str]:
        if s is None:
            return None
        st = str(s).strip()
        return st if st else None

    return {
        "brand": _c(brand),
        "model": _c(model),
        "variant": _c(variant),
        "manufacture_year": manufacture_year,
        "price": price if price is not None else None,
        "mileage": _c(mileage),
        "fuel_type": _c(fuel_type),
        "transmission": _c(transmission),
        "body_type": _c(body_type),
        "location": _c(location),
        "source_url": clean_source_url,
        "image_url": _c(image_url),
        "listed_at": _c(listed_at),
        "crawled_at": crawled_at,
    }
