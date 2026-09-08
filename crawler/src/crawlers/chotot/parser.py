"""
Chợ Tốt HTML Parser module.
Responsible for extracting listing URLs and parsing detail page data
strictly into the 14-field project data contract.
"""

from datetime import datetime, timezone
import json
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup

BASE_URL = "https://xe.chotot.com"
LISTING_URL_PATTERN = re.compile(r"/(\d+)\.htm", re.IGNORECASE)
YEAR_PATTERN = re.compile(r"\b(19\d{2}|20\d{2})\b")


def normalize_url(url: str, base: str = BASE_URL) -> str:
    """
    Normalize Chợ Tốt detail URL by stripping tracking parameters, fragments,
    and converting relative URLs to absolute URLs.
    """
    if not url:
        return ""
    full_url = urljoin(base, url.strip())
    parsed = urlparse(full_url)
    # Rebuild without query parameters and fragment
    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
    return clean_url


def is_valid_detail_url(url: str) -> bool:
    """
    Check if URL matches a valid Chợ Tốt vehicle detail URL pattern.
    """
    if not url:
        return False
    return bool(LISTING_URL_PATTERN.search(url))


def extract_listing_urls(html: str, base: str = BASE_URL) -> List[str]:
    """
    Extract and deduplicate vehicle detail URLs from a rendered listing page HTML.
    """
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    found_urls: List[str] = []
    seen: set = set()

    # Find <a> tags with href containing /<id>.htm
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if LISTING_URL_PATTERN.search(href):
            norm = normalize_url(href, base=base)
            if norm and norm not in seen:
                seen.add(norm)
                found_urls.append(norm)

    # Fallback regex search if soup missed dynamic hrefs
    if not found_urls:
        matches = re.findall(r'href=["\'](/[^"\']+/\d+\.htm[^"\']*)["\']', html)
        for m in matches:
            norm = normalize_url(m, base=base)
            if norm and norm not in seen:
                seen.add(norm)
                found_urls.append(norm)

    return found_urls


def _parse_year(val: Any) -> Optional[int]:
    """Safely parse year to integer."""
    if val is None:
        return None
    s = str(val).strip()
    match = YEAR_PATTERN.search(s)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None


def _clean_str(val: Any) -> Optional[str]:
    """Clean string value or return None if empty."""
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None


def _extract_json_ld_car(soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
    """Extract Car / Product JSON-LD metadata if present."""
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        if not script.string:
            continue
        try:
            data = json.loads(script.string.strip())
            # Handle list of schemas or single schema
            schemas = data if isinstance(data, list) else [data]
            for schema in schemas:
                if not isinstance(schema, dict):
                    continue
                stype = schema.get("@type", [])
                if isinstance(stype, str):
                    stype = [stype]
                if any(t in ["Car", "Product", "Vehicle"] for t in stype):
                    return schema
        except Exception:
            continue
    return None


def _extract_itemprops(soup: BeautifulSoup) -> Dict[str, str]:
    """Extract all elements with itemprop attributes."""
    result: Dict[str, str] = {}
    for elem in soup.find_all(attrs={"itemprop": True}):
        prop = elem.get("itemprop")
        if not prop:
            continue
        # Content attribute or inner text
        content = elem.get("content")
        if content:
            val = content.strip()
        else:
            val = elem.get_text(separator=" ", strip=True)
        if val and prop not in result:
            result[prop] = val
    return result


def _extract_label_value_pairs(soup: BeautifulSoup) -> Dict[str, str]:
    """Extract key-value pairs from parameter display blocks."""
    pairs: Dict[str, str] = {}
    # Common Chợ Tốt container classes: div.p1ja3eq0 or containers with two spans
    for container in soup.find_all("div", class_=re.compile(r"p1ja3eq0|adParam|paramsBlock")):
        spans = container.find_all("span")
        if len(spans) >= 2:
            lbl = spans[0].get_text(strip=True).lower()
            val = spans[1].get_text(strip=True)
            if lbl and val:
                pairs[lbl] = val

    # Also search general spans or definition terms
    if not pairs:
        for span in soup.find_all("span", class_="bwq0cbs"):
            parent = span.parent
            if parent:
                sibling_spans = parent.find_all("span")
                if len(sibling_spans) >= 2:
                    lbl = sibling_spans[0].get_text(strip=True).lower()
                    val = sibling_spans[1].get_text(strip=True)
                    if lbl and val and lbl not in pairs:
                        pairs[lbl] = val
    return pairs


def _find_by_labels(pairs: Dict[str, str], patterns: List[str]) -> Optional[str]:
    """Find a value from pairs dictionary matching label patterns."""
    for lbl, val in pairs.items():
        for pat in patterns:
            if re.search(pat, lbl, re.IGNORECASE):
                return val
    return None


def _extract_listed_at(soup: BeautifulSoup, html: str) -> Optional[str]:
    """Extract listing date or relative time string."""
    # Pattern 1: Regex on raw HTML
    match = re.search(r"(?:[Đđ]ăng|posted)\s*(?:<!--.*?-->)?\s*([^<\n\r]+)", html, re.IGNORECASE)
    if match:
        text = match.group(1).strip()
        if text and len(text) < 50 and any(kw in text.lower() for kw in ["trước", "hôm", "ngày", "tháng", "giờ"]):
            return text

    # Pattern 2: span elements containing "trước" or "hôm"
    for span in soup.find_all(["span", "p", "div"]):
        txt = span.get_text(strip=True)
        if any(w in txt.lower() for w in ["trước", "hôm nay", "hôm qua"]):
            cleaned = re.sub(r"^(?:[Đđ]ăng|posted)\s*", "", txt, flags=re.IGNORECASE).strip()
            if re.search(r"^\d+\s*(?:giờ|phút|ngày|tuần|tháng)\s*trước$", cleaned, re.IGNORECASE):
                return cleaned
            if cleaned.lower() in ["hôm nay", "hôm qua"]:
                return cleaned

    # Pattern 3: meta published time
    meta_date = soup.find("meta", attrs={"property": "article:published_time"}) or soup.find(
        "meta", attrs={"name": "date"}
    )
    if meta_date and meta_date.get("content"):
        return meta_date["content"].strip()

    return None


def _extract_image_url(soup: BeautifulSoup, json_ld: Optional[Dict[str, Any]]) -> Optional[str]:
    """Extract primary vehicle image URL."""
    # From JSON-LD
    if json_ld:
        img_data = json_ld.get("image")
        if isinstance(img_data, list) and len(img_data) > 0:
            first = img_data[0]
            if isinstance(first, dict) and "url" in first:
                return first["url"]
            elif isinstance(first, str):
                return first
        elif isinstance(img_data, dict) and "url" in img_data:
            return img_data["url"]
        elif isinstance(img_data, str):
            return img_data

    # From meta og:image
    meta_img = soup.find("meta", attrs={"property": "og:image"})
    if meta_img and meta_img.get("content"):
        return meta_img["content"].strip()

    return None


def parse_detail_page(
    html: str, source_url: str, crawled_at: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Parse a Chợ Tốt vehicle detail page HTML into the authoritative 14-field record.
    Returns None if the page is invalid or missing required identifiers.
    """
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    json_ld = _extract_json_ld_car(soup)
    itemprops = _extract_itemprops(soup)
    pairs = _extract_label_value_pairs(soup)

    # 1. brand
    brand = None
    if json_ld and json_ld.get("brand"):
        b = json_ld["brand"]
        brand = b.get("name") if isinstance(b, dict) else b
    if not brand:
        brand = itemprops.get("carbrand")
    if not brand:
        brand = _find_by_labels(pairs, [r"hãng", r"thương hiệu"])

    # 2. model
    model = None
    if json_ld and json_ld.get("model"):
        model = json_ld["model"]
    if not model:
        model = itemprops.get("carmodel")
    if not model:
        model = _find_by_labels(pairs, [r"dòng xe", r"model"])

    # 3. variant
    variant = itemprops.get("option")
    if not variant:
        variant = _find_by_labels(pairs, [r"phiên bản", r"bản"])

    # 4. manufacture_year
    year_val = None
    if json_ld and json_ld.get("vehicleModelDate"):
        year_val = json_ld["vehicleModelDate"]
    if not year_val:
        year_val = itemprops.get("mfdate")
    if not year_val:
        year_val = _find_by_labels(pairs, [r"năm sản xuất", r"năm sx"])
    manufacture_year = _parse_year(year_val)

    # 5. price
    price = None
    if json_ld and json_ld.get("offers"):
        offers = json_ld["offers"]
        if isinstance(offers, dict):
            price = offers.get("price")
    if price is None:
        price = itemprops.get("price")
    if price is None:
        price_tag = soup.find("b", class_=re.compile(r"p26z2wb|price"))
        if price_tag:
            price = price_tag.get_text(strip=True)

    # 6. mileage
    mileage = None
    if json_ld and json_ld.get("mileageFromOdometer"):
        m_odo = json_ld["mileageFromOdometer"]
        if isinstance(m_odo, dict):
            mileage = m_odo.get("value")
        else:
            mileage = m_odo
    if mileage is None:
        mileage = itemprops.get("mileage_v2") or itemprops.get("mileage")
    if mileage is None:
        mileage = _find_by_labels(pairs, [r"số km đã đi", r"số km", r"km đã đi", r"odo"])

    # 7. fuel_type
    fuel_type = None
    if json_ld and json_ld.get("vehicleEngine"):
        eng = json_ld["vehicleEngine"]
        if isinstance(eng, dict):
            fuel_type = eng.get("fuelType")
    if not fuel_type:
        fuel_type = itemprops.get("fuel")
    if not fuel_type:
        fuel_type = _find_by_labels(pairs, [r"nhiên liệu"])

    # 8. transmission
    transmission = None
    if json_ld and json_ld.get("vehicleTransmission"):
        transmission = json_ld["vehicleTransmission"]
    if not transmission:
        transmission = itemprops.get("gearbox")
    if not transmission:
        transmission = _find_by_labels(pairs, [r"hộp số"])

    # 9. body_type
    body_type = None
    if json_ld and json_ld.get("bodyType"):
        body_type = json_ld["bodyType"]
    if not body_type:
        body_type = itemprops.get("cartype")
    if not body_type:
        body_type = _find_by_labels(pairs, [r"kiểu dáng", r"kiểu xe"])

    # 10. location
    location = None
    if json_ld and json_ld.get("offers"):
        offers = json_ld["offers"]
        if isinstance(offers, dict):
            location = offers.get("areaServed")
    if not location:
        location = itemprops.get("addressLocality")
    if not location:
        location = _find_by_labels(pairs, [r"khu vực", r"tỉnh thành", r"địa chỉ"])
    if not location:
        loc_span = soup.find("span", class_=re.compile(r"flex-1|address"))
        if loc_span:
            txt = loc_span.get_text(strip=True)
            if "," in txt and "đăng" not in txt.lower():
                location = txt

    # 11. source_url
    clean_source_url = normalize_url(source_url)

    # 12. image_url
    image_url = _extract_image_url(soup, json_ld)

    # 13. listed_at
    listed_at = _extract_listed_at(soup, html)

    # 14. crawled_at
    if not crawled_at:
        crawled_at = datetime.now(timezone.utc).isoformat()

    # Minimum validation: must have source_url and at least brand or model or price
    if not clean_source_url or (not brand and not model and not price):
        return None

    # Construct exactly the 14 fields
    return {
        "brand": _clean_str(brand),
        "model": _clean_str(model),
        "variant": _clean_str(variant),
        "manufacture_year": manufacture_year,
        "price": price if price is not None else None,
        "mileage": _clean_str(mileage),
        "fuel_type": _clean_str(fuel_type),
        "transmission": _clean_str(transmission),
        "body_type": _clean_str(body_type),
        "location": _clean_str(location),
        "source_url": clean_source_url,
        "image_url": _clean_str(image_url),
        "listed_at": _clean_str(listed_at),
        "crawled_at": crawled_at,
    }
