"""
Validator Module for Phase 4.
Validates cleaned vehicle records against schema contract and basic integrity constraints.
"""

from typing import Any, Dict, List, Tuple

CANONICAL_FIELDS = [
    "brand",
    "model",
    "variant",
    "manufacture_year",
    "price",
    "mileage",
    "fuel_type",
    "transmission",
    "body_type",
    "location",
    "source_url",
    "image_url",
    "listed_at",
    "crawled_at",
]

EXPECTED_TYPES = {
    "brand": (str, type(None)),
    "model": (str, type(None)),
    "variant": (str, type(None)),
    "manufacture_year": (int, type(None)),
    "price": (int, type(None)),
    "mileage": (int, type(None)),
    "fuel_type": (str, type(None)),
    "transmission": (str, type(None)),
    "body_type": (str, type(None)),
    "location": (str, type(None)),
    "source_url": (str,),
    "image_url": (str, type(None)),
    "listed_at": (str, type(None)),
    "crawled_at": (str,),
}


def validate_cleaned_record(record: dict, record_idx: int = 0) -> Tuple[bool, List[str]]:
    """
    Validates a single cleaned record against the 14-field contract and expected types.
    """
    errors = []

    # Check key presence and ordering
    if list(record.keys()) != CANONICAL_FIELDS:
        missing = [f for f in CANONICAL_FIELDS if f not in record]
        extra = [f for f in record if f not in CANONICAL_FIELDS]
        if missing:
            errors.append(f"Record #{record_idx}: Missing fields: {missing}")
        if extra:
            errors.append(f"Record #{record_idx}: Extra fields: {extra}")

    # Check data types
    for field, expected_type in EXPECTED_TYPES.items():
        val = record.get(field)
        if not isinstance(val, expected_type):
            errors.append(f"Record #{record_idx}: Field '{field}' expected {expected_type}, got {type(val).__name__} ({repr(val)})")

    # Critical non-null fields
    if not record.get("source_url"):
        errors.append(f"Record #{record_idx}: source_url must not be empty")
    if not record.get("crawled_at"):
        errors.append(f"Record #{record_idx}: crawled_at must not be empty")

    return len(errors) == 0, errors


def validate_dataset(records: List[dict]) -> Tuple[bool, Dict[str, Any]]:
    """
    Validates the entire cleaned dataset.
    Returns (is_valid, validation_summary).
    """
    total_records = len(records)
    total_errors = 0
    sample_errors = []
    unique_urls = set()
    null_counts = {field: 0 for field in CANONICAL_FIELDS}

    for idx, rec in enumerate(records):
        valid, errs = validate_cleaned_record(rec, idx)
        if not valid:
            total_errors += len(errs)
            if len(sample_errors) < 10:
                sample_errors.extend(errs)

        url = rec.get("source_url")
        if url:
            unique_urls.add(url)

        for field in CANONICAL_FIELDS:
            if rec.get(field) is None:
                null_counts[field] += 1

    summary = {
        "total_records": total_records,
        "unique_source_urls": len(unique_urls),
        "total_validation_errors": total_errors,
        "sample_errors": sample_errors,
        "null_counts": null_counts,
        "is_schema_contract_valid": (total_errors == 0),
        "is_url_unique": (len(unique_urls) == total_records),
    }

    return (total_errors == 0 and len(unique_urls) == total_records), summary
