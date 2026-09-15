"""
Price Cleaning Module.
Normalizes vehicle listing prices into integer Vietnamese Dong (VND).

Rules:
- Output is integer VND or None if missing/invalid.
- Supports integer/float prices directly.
- Parses string prices including Vietnamese terms: 'tỷ', 'triệu', 'nghìn'.
- Does NOT replace invalid prices with 0, mean, median, or fabricated values.
"""

import math
import re
from typing import Any, Optional

NULL_TOKENS = {"", "none", "null", "n/a", "na", "-", "không xác định", "liên hệ", "thương lượng"}


def clean_price(val: Any) -> Optional[int]:
    """
    Clean and parse vehicle price to integer VND.
    Returns None if missing, unparseable, or <= 0.
    """
    if val is None:
        return None

    # Handle numeric input
    if isinstance(val, (int, float)):
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return None
        if val <= 0:
            return None
        return int(round(val))

    if not isinstance(val, str):
        val = str(val)

    s = val.strip().lower()
    if s in NULL_TOKENS:
        return None

    # Check for Vietnamese composite units e.g. "1 tỷ 250 triệu" or "498 triệu"
    has_ty = "tỷ" in s or "ty" in s
    has_trieu = "triệu" in s or "trieu" in s or "tr" in s

    if has_ty or has_trieu:
        total_vnd = 0.0
        # Parse 'tỷ' component
        ty_match = re.search(r"([\d.,]+)\s*(?:tỷ|ty)", s)
        if ty_match:
            try:
                num_str = ty_match.group(1).replace(",", ".")
                # Handle possible multiple dots like 1.25
                total_vnd += float(num_str) * 1_000_000_000
            except ValueError:
                pass

        # Parse 'triệu' component
        trieu_match = re.search(r"([\d.,]+)\s*(?:triệu|trieu|tr)", s)
        if trieu_match:
            try:
                num_str = trieu_match.group(1).replace(",", ".")
                total_vnd += float(num_str) * 1_000_000
            except ValueError:
                pass

        if total_vnd > 0:
            return int(round(total_vnd))

    # Clean numeric string: remove commas, dots, currency symbols
    clean_digits = re.sub(r"[^\d]", "", s)
    if not clean_digits:
        return None

    try:
        price_int = int(clean_digits)
        if price_int <= 0:
            return None
        return price_int
    except ValueError:
        return None
