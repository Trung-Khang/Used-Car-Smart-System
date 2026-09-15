"""
Seed Database CLI Wrapper Script.
Runs the Phase 6 Import Pipeline to generate seeds and import into PostgreSQL.

Author: TV3 — Data Engineering / Data Pipeline Developer
Project: Used-Car-Smart-System
"""

import sys
from pathlib import Path

# Add crawler/src to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CRAWLER_SRC = PROJECT_ROOT / "crawler" / "src"

if str(CRAWLER_SRC) not in sys.path:
    sys.path.insert(0, str(CRAWLER_SRC))

from pipeline.import_pipeline import main

if __name__ == "__main__":
    main()
