"""
Cleaning and Normalization Module - Phase 4.
Contains specialized cleaners for vehicle listings attributes and dataset validation.
"""

from .clean_price import clean_price
from .clean_mileage import clean_mileage
from .clean_vehicle import (
    clean_brand,
    clean_model,
    clean_variant,
    clean_year,
    clean_transmission,
    clean_fuel_type,
    clean_body_type,
    clean_location,
    clean_listed_at,
    clean_image_url,
    clean_source_url,
    clean_crawled_at,
    clean_vehicle_record,
    BRAND_MAPPING,
    TRANSMISSION_MAPPING,
    FUEL_TYPE_MAPPING,
    BODY_TYPE_MAPPING,
    PROVINCE_MAPPING,
)
from .validator import validate_cleaned_record, validate_dataset

__all__ = [
    "clean_price",
    "clean_mileage",
    "clean_brand",
    "clean_model",
    "clean_variant",
    "clean_year",
    "clean_transmission",
    "clean_fuel_type",
    "clean_body_type",
    "clean_location",
    "clean_listed_at",
    "clean_image_url",
    "clean_source_url",
    "clean_crawled_at",
    "clean_vehicle_record",
    "BRAND_MAPPING",
    "TRANSMISSION_MAPPING",
    "FUEL_TYPE_MAPPING",
    "BODY_TYPE_MAPPING",
    "PROVINCE_MAPPING",
    "validate_cleaned_record",
    "validate_dataset",
]
