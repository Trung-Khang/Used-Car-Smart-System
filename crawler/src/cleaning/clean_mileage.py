"""
Mileage Cleaning Module.
Normalizes vehicle odometer reading into integer kilometers.

Rules:
- Output is integer km or None if missing/invalid.
- Supports integer/float mileages directly.
- Handles Vietnamese thousands separators (both '.' and ',') appropriately.
  In Vietnamese listings, "16,000 Km" and "92.000" both represent thousands.
- Handles Vietnamese unit terms such as "vạn" (1 vạn = 10,000 km).
- Outlier detection and handling belongs to Phase 5; Phase 4 faithfully parses observed integers.
- Does NOT fabricate missing values.
"""

import math
import re
from typing import Any, Optional

NULL_TOKENS = {"", "none", "null", "n/a", "na", "-", "không xác định", "chưa xác định"}


def clean_mileage(val: Any) -> Optional[int]:
    """
    Clean and parse vehicle mileage to integer kilometers.
    Returns None if missing, unparseable, or negative.
    """
    if val is None:
        return None

    if isinstance(val, (int, float)):
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return None
        if val < 0:
            return None
        return int(round(val))

    if not isinstance(val, str):
        val = str(val)

    s = val.strip().lower()
    if s in NULL_TOKENS:
        return None

    # Handle "vạn" e.g. "5 vạn" -> 50,000 km
    van_match = re.search(r"([\d.,]+)\s*vạn", s)
    if van_match:
        try:
            num = float(van_match.group(1).replace(",", "."))
            return int(round(num * 10_000))
        except ValueError:
            pass

    # Remove unit words like km, k
    s_clean = re.sub(r"(?:km|k\b)", "", s).strip()

    # Remove all formatting separators (dots and commas are thousands separators in VN auto listings)
    # E.g. "16,000" -> "16000", "92.000" -> "92000", "113.456" -> "113456"
    digits_only = re.sub(r"[^\d]", "", s_clean)
    if not digits_only:
        return None

    try:
        km = int(digits_only)
        if km < 0:
            return None
        return km
    except ValueError:
        return None
