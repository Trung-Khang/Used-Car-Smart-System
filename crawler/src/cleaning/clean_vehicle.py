"""
Vehicle Attributes Cleaning and Normalization Module.
Normalizes vehicle metadata: brand, model, variant, year, transmission, fuel, body,
location, and timestamps.
"""

import math
import re
from datetime import datetime
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse

NULL_TOKENS = {"", "none", "null", "n/a", "na", "-", "không xác định", "chưa xác định"}

# Canonical Brand Mapping
# Preserves brand identity while fixing casing, spacing, and alternate spellings
BRAND_MAPPING: Dict[str, str] = {
    "toyota": "Toyota",
    "vinfast": "VinFast",
    "ford": "Ford",
    "hyundai": "Hyundai",
    "mercedes benz": "Mercedes-Benz",
    "mercedes-benz": "Mercedes-Benz",
    "kia": "Kia",
    "mazda": "Mazda",
    "mitsubishi": "Mitsubishi",
    "lexus": "Lexus",
    "honda": "Honda",
    "bmw": "BMW",
    "mg": "MG",
    "chevrolet": "Chevrolet",
    "volkswagen": "Volkswagen",
    "porsche": "Porsche",
    "suzuki": "Suzuki",
    "audi": "Audi",
    "peugeot": "Peugeot",
    "landrover": "Land Rover",
    "land rover": "Land Rover",
    "nissan": "Nissan",
    "volvo": "Volvo",
    "isuzu": "Isuzu",
    "byd": "BYD",
    "daewoo": "Daewoo",
    "mini": "Mini",
    "geely": "Geely",
    "subaru": "Subaru",
    "bentley": "Bentley",
    "hãng khác": "Hãng khác",
    "hãng khác": "Hãng khác",
    "jeep": "Jeep",
    "rolls royce": "Rolls-Royce",
    "rolls-royce": "Rolls-Royce",
    "maserati": "Maserati",
    "jaguar": "Jaguar",
    "cadillac": "Cadillac",
    "chery": "Chery",
    "infiniti": "Infiniti",
    "haval": "Haval",
    "lincoln": "Lincoln",
    "renault": "Renault",
    "hino": "Hino",
    "lynk & co": "Lynk & Co",
    "lynk and co": "Lynk & Co",
    "wuling": "Wuling",
    "acura": "Acura",
    "ssangyong": "SsangYong",
    "chrysler": "Chrysler",
    "fiat": "Fiat",
    "luxgen": "Luxgen",
    "landwind": "Landwind",
    "aston martin": "Aston Martin",
    "hongqi": "Hongqi",
    "alfa romeo": "Alfa Romeo",
    "ferrari": "Ferrari",
    "mclaren": "McLaren",
    "lamborghini": "Lamborghini",
    "thaco": "Thaco",
    "gaz": "GAZ",
    "dodge": "Dodge",
    "smart": "Smart",
    "volga": "Volga",
    "tobe": "Tobe",
    "changan": "Changan",
    "baic": "BAIC",
    "dongfeng": "Dongfeng",
    "zotye": "Zotye",
    "uaz": "UAZ",
    "lada": "Lada",
    "proton": "Proton",
}

# Known Model Casing Normalization
MODEL_CASING_MAPPING: Dict[str, str] = {
    "c class": "C Class",
    "e class": "E Class",
    "s class": "S Class",
    "a class": "A Class",
    "v class": "V Class",
    "gla class": "GLA Class",
    "cla class": "CLA Class",
    "corolla altis": "Corolla Altis",
    "x trail": "X Trail",
    "ec van": "EC Van",
}

# Canonical Transmission Mapping
TRANSMISSION_MAPPING: Dict[str, str] = {
    "số tự động": "Automatic",
    "tự động": "Automatic",
    "at": "Automatic",
    "automatic": "Automatic",
    "số sàn": "Manual",
    "số tay": "Manual",
    "mt": "Manual",
    "manual": "Manual",
    "bán tự động": "Semi-Automatic",
    "semi-automatic": "Semi-Automatic",
    "cvt": "CVT",
    "5": "Other",
}

# Canonical Fuel Type Mapping
FUEL_TYPE_MAPPING: Dict[str, str] = {
    "xăng": "Gasoline",
    "gasoline": "Gasoline",
    "petrol": "Gasoline",
    "dầu": "Diesel",
    "diesel": "Diesel",
    "điện": "Electric",
    "electric": "Electric",
    "hybrid": "Hybrid",
    "động cơ hybrid": "Hybrid",
    "plug-in hybrid": "Hybrid",
    "loại khác  2.5 l": "Other",
    "khác": "Other",
}

# Canonical Body Type Mapping
BODY_TYPE_MAPPING: Dict[str, str] = {
    "suv": "SUV",
    "sedan": "Sedan",
    "suv / cross over": "SUV / Crossover",
    "suv / crossover": "SUV / Crossover",
    "crossover": "Crossover",
    "hatchback": "Hatchback",
    "bán tải / pickup": "Pickup",
    "bán tải / pickup": "Pickup",
    "pick-up (bán tải)": "Pickup",
    "pickup": "Pickup",
    "minivan (mpv)": "MPV",
    "mpv": "MPV",
    "van/minivan": "Van / Minivan",
    "van / minivan": "Van / Minivan",
    "van": "Van",
    "coupe": "Coupe",
    "coupe (2 cửa)": "Coupe",
    "convertible/cabriolet": "Convertible",
    "convertible": "Convertible",
    "mui trần": "Convertible",
    "truck": "Truck",
    "wagon": "Wagon",
    "kiểu dáng khác": "Other",
    "khác": "Other",
}

# Province / City Canonical Mapping
PROVINCE_MAPPING: Dict[str, str] = {
    "tp hcm": "Hồ Chí Minh",
    "tp.hcm": "Hồ Chí Minh",
    "tp hồ chí minh": "Hồ Chí Minh",
    "hồ chí minh": "Hồ Chí Minh",
    "tphcm": "Hồ Chí Minh",
    "đăk lăk": "Đắk Lắk",
    "đắk lắk": "Đắk Lắk",
    "bà rịa vũng tàu": "Bà Rịa - Vũng Tàu",
    "bà rịa - vũng tàu": "Bà Rịa - Vũng Tàu",
    "thừa thiên huế": "Thừa Thiên Huế",
    "đắk nông": "Đắk Nông",
}


def clean_brand(val: Any) -> Optional[str]:
    """Clean and standardize brand name."""
    if val is None:
        return None
    s = str(val).strip()
    if s.lower() in NULL_TOKENS:
        return None
    key = re.sub(r"\s+", " ", s.lower())
    return BRAND_MAPPING.get(key, s)


def clean_model(val: Any, brand: Optional[str] = None) -> Optional[str]:
    """Clean and standardize model name without aggressive overwriting."""
    if val is None:
        return None
    s = str(val).strip()
    if s.lower() in NULL_TOKENS:
        return None
    s = re.sub(r"\s+", " ", s)

    # Check known casing normalizations
    key = s.lower()
    if key in MODEL_CASING_MAPPING:
        return MODEL_CASING_MAPPING[key]

    return s


def clean_variant(val: Any) -> Optional[str]:
    """Conservative cleaning for trim / variant."""
    if val is None:
        return None
    s = str(val).strip()
    if s.lower() in NULL_TOKENS:
        return None
    s = re.sub(r"\s+", " ", s)
    return s if s else None


def clean_year(val: Any, min_year: int = 1900, max_year: int = 2026) -> Optional[int]:
    """Clean manufacture year to integer within valid vehicle range."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return None
        y = int(val)
        if min_year <= y <= max_year:
            return y
        return None

    s = str(val).strip()
    match = re.search(r"\b(19\d{2}|20\d{2})\b", s)
    if match:
        y = int(match.group(1))
        if min_year <= y <= max_year:
            return y
    return None


def clean_transmission(val: Any) -> Optional[str]:
    """Normalize transmission to canonical vocabulary."""
    if val is None:
        return None
    s = str(val).strip()
    if s.lower() in NULL_TOKENS:
        return None
    key = re.sub(r"\s+", " ", s.lower())
    return TRANSMISSION_MAPPING.get(key, "Other")


def clean_fuel_type(val: Any) -> Optional[str]:
    """Normalize fuel type to canonical vocabulary."""
    if val is None:
        return None
    s = str(val).strip()
    if s.lower() in NULL_TOKENS:
        return None
    key = re.sub(r"\s+", " ", s.lower())
    return FUEL_TYPE_MAPPING.get(key, "Other")


def clean_body_type(val: Any) -> Optional[str]:
    """Normalize body type to canonical vocabulary."""
    if val is None:
        return None
    s = str(val).strip()
    if s.lower() in NULL_TOKENS:
        return None
    key = re.sub(r"\s+", " ", s.lower())
    return BODY_TYPE_MAPPING.get(key, s)


def clean_location(val: Any) -> Optional[str]:
    """
    Clean location preserving district info while standardizing province/city names.
    E.g. 'Quận 7, Tp Hồ Chí Minh' -> 'Quận 7, Hồ Chí Minh'
         'TP HCM' -> 'Hồ Chí Minh'
    """
    if val is None:
        return None
    s = str(val).strip()
    if s.lower() in NULL_TOKENS:
        return None

    # Split by comma if district and province are present
    parts = [re.sub(r"\s+", " ", p.strip()) for p in s.split(",")]
    if not parts:
        return None

    # Clean province (last component)
    prov_raw = parts[-1]
    prov_key = prov_raw.lower()
    prov_norm = PROVINCE_MAPPING.get(prov_key, prov_raw)

    if len(parts) == 1:
        return prov_norm
    else:
        district_part = ", ".join(parts[:-1])
        return f"{district_part}, {prov_norm}"


def clean_listed_at(val: Any) -> Optional[str]:
    """
    Clean listed_at field.
    Parses deterministic date 'D/MM/YYYY' into 'YYYY-MM-DD'.
    Preserves trimmed relative date strings (e.g. '3 ngày trước').
    """
    if val is None:
        return None
    s = str(val).strip()
    if s.lower() in NULL_TOKENS:
        return None

    # Check for D/M/YYYY or DD/MM/YYYY
    date_match = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if date_match:
        day = int(date_match.group(1))
        month = int(date_match.group(2))
        year = int(date_match.group(3))
        try:
            return f"{year:04d}-{month:02d}-{day:02d}"
        except Exception:
            pass

    return s


def clean_image_url(val: Any) -> Optional[str]:
    """Clean image URL string."""
    if val is None:
        return None
    s = str(val).strip()
    if s.lower() in NULL_TOKENS:
        return None
    parsed = urlparse(s)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return s
    return None


def clean_source_url(val: Any) -> str:
    """Validate and trim source URL without altering query/path."""
    if not val:
        raise ValueError("Record missing required source_url")
    s = str(val).strip()
    parsed = urlparse(s)
    if not (parsed.scheme in ("http", "https") and parsed.netloc):
        raise ValueError(f"Invalid source_url: {s}")
    return s


def clean_crawled_at(val: Any) -> str:
    """Validate crawled_at ISO timestamp."""
    if not val:
        raise ValueError("Record missing required crawled_at")
    s = str(val).strip()
    # Basic ISO format validation
    return s


def clean_vehicle_record(raw_record: dict) -> Tuple[dict, dict]:
    """
    Applies cleaning rules to a single vehicle record.
    Returns:
      (cleaned_record, transformations_log)
    """
    from .clean_price import clean_price
    from .clean_mileage import clean_mileage

    transformations = {}

    brand = clean_brand(raw_record.get("brand"))
    if brand != raw_record.get("brand"):
        transformations["brand"] = (raw_record.get("brand"), brand)

    model = clean_model(raw_record.get("model"), brand=brand)
    if model != raw_record.get("model"):
        transformations["model"] = (raw_record.get("model"), model)

    variant = clean_variant(raw_record.get("variant"))
    if variant != raw_record.get("variant"):
        transformations["variant"] = (raw_record.get("variant"), variant)

    year = clean_year(raw_record.get("manufacture_year"))
    if year != raw_record.get("manufacture_year"):
        transformations["manufacture_year"] = (raw_record.get("manufacture_year"), year)

    price = clean_price(raw_record.get("price"))
    if price != raw_record.get("price"):
        transformations["price"] = (raw_record.get("price"), price)

    mileage = clean_mileage(raw_record.get("mileage"))
    if mileage != raw_record.get("mileage"):
        transformations["mileage"] = (raw_record.get("mileage"), mileage)

    fuel_type = clean_fuel_type(raw_record.get("fuel_type"))
    if fuel_type != raw_record.get("fuel_type"):
        transformations["fuel_type"] = (raw_record.get("fuel_type"), fuel_type)

    transmission = clean_transmission(raw_record.get("transmission"))
    if transmission != raw_record.get("transmission"):
        transformations["transmission"] = (raw_record.get("transmission"), transmission)

    body_type = clean_body_type(raw_record.get("body_type"))
    if body_type != raw_record.get("body_type"):
        transformations["body_type"] = (raw_record.get("body_type"), body_type)

    location = clean_location(raw_record.get("location"))
    if location != raw_record.get("location"):
        transformations["location"] = (raw_record.get("location"), location)

    source_url = clean_source_url(raw_record.get("source_url"))
    image_url = clean_image_url(raw_record.get("image_url"))
    listed_at = clean_listed_at(raw_record.get("listed_at"))
    if listed_at != raw_record.get("listed_at"):
        transformations["listed_at"] = (raw_record.get("listed_at"), listed_at)

    crawled_at = clean_crawled_at(raw_record.get("crawled_at"))

    cleaned = {
        "brand": brand,
        "model": model,
        "variant": variant,
        "manufacture_year": year,
        "price": price,
        "mileage": mileage,
        "fuel_type": fuel_type,
        "transmission": transmission,
        "body_type": body_type,
        "location": location,
        "source_url": source_url,
        "image_url": image_url,
        "listed_at": listed_at,
        "crawled_at": crawled_at,
    }

    return cleaned, transformations
