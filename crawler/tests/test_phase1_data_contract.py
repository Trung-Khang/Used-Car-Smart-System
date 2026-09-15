import json
import sys
import unittest
from pathlib import Path

CRAWLER_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(CRAWLER_SRC))

from cleaning.clean_vehicle import clean_body_type, clean_fuel_type, clean_transmission, clean_vehicle_record
from cleaning.validator import (
    CANONICAL_FIELDS,
    DATA_CONTRACT_VERSION,
    PRE_ENRICHMENT_FIELDS,
    validate_dataset,
)
from pipeline.import_pipeline import SEED_FIELDS, transform_record_for_database


ROOT = Path(__file__).resolve().parents[1]
CLEANED = ROOT / "data" / "cleaned" / "vehicles_cleaned.json"
SEED = ROOT / "data" / "seed" / "vehicles_seed.json"


class Phase1ContractTest(unittest.TestCase):
    def test_contract_boundary(self):
        self.assertEqual(DATA_CONTRACT_VERSION, "1.0.0")
        self.assertEqual(len(PRE_ENRICHMENT_FIELDS), 14)
        self.assertEqual(len(CANONICAL_FIELDS), 17)
        self.assertEqual(CANONICAL_FIELDS[:10], PRE_ENRICHMENT_FIELDS[:10])

    def test_normalization_rules(self):
        self.assertEqual(clean_body_type("SUV"), "SUV / Crossover")
        self.assertEqual(clean_body_type("Crossover"), "SUV / Crossover")
        self.assertEqual(clean_body_type("Van / Minivan"), "Van")
        self.assertIsNone(clean_body_type("Khác"))
        self.assertIsNone(clean_fuel_type("khác"))
        self.assertIsNone(clean_transmission("5"))

    def test_enrichment_fields_are_preserved(self):
        raw = {
            "brand": "Toyota", "model": "Camry", "variant": "2.5Q",
            "manufacture_year": 2020, "price": 850000000, "mileage": 45000,
            "fuel_type": "Xăng", "transmission": "Số tự động",
            "body_type": "Sedan", "location": "Hà Nội",
            "origin": "Imported", "engine_size": 2.5, "seat_count": 5,
            "source_url": "https://example.com/1", "image_url": "https://example.com/i.jpg",
            "listed_at": "2026-09-07", "crawled_at": "2026-09-07T08:25:55+00:00",
        }
        cleaned, _ = clean_vehicle_record(raw)
        self.assertEqual(list(cleaned), CANONICAL_FIELDS)
        self.assertEqual(cleaned["origin"], "Imported")
        self.assertEqual(cleaned["engine_size"], 2.5)
        self.assertEqual(cleaned["seat_count"], 5)

    def test_final_dataset_passes_contract(self):
        records = json.loads(CLEANED.read_text(encoding="utf-8"))
        ok, summary = validate_dataset(records)
        self.assertTrue(ok, summary)
        self.assertEqual(summary["total_records"], 10813)
        self.assertEqual(summary["unique_source_urls"], 10813)
        self.assertEqual(summary["duplicate_source_urls"], 0)
        self.assertEqual(summary["total_validation_errors"], 0)

    def test_seed_preserves_all_contract_fields(self):
        records = json.loads(CLEANED.read_text(encoding="utf-8"))
        seeds = json.loads(SEED.read_text(encoding="utf-8"))
        self.assertEqual(len(seeds), len(records))
        self.assertEqual(len(SEED_FIELDS), 19)
        for record, seed in zip(records[:100], seeds[:100]):
            for field in CANONICAL_FIELDS:
                self.assertEqual(seed[field], record[field], field)
            self.assertIn(seed["source"], {"chotot", "bonbanh"})


if __name__ == "__main__":
    unittest.main()
