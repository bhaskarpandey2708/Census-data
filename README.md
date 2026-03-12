# Census Data Pipeline (India, Census 2011)

This repository now includes a practical starter kit to begin **data mining and scraping** for Census 2011 and prepare a clean analytics-ready dataset.

## Scope
- Geography hierarchy: State → District → Block → Gram Panchayat → Village
- Demographic indicators (2011):
  - Total population
  - Male / Female
  - SC / ST
  - Rural / Urban
  - Religion (Hindu, Muslim)

## Repository Structure
- `data/raw/census2011/` - downloaded source files from official portals
- `data/staging/` - normalized/staging extracts
- `data/curated/` - conformed outputs
- `sql/ddl/` - table definitions
- `sql/transforms/` - merge/upsert transform logic
- `scripts/` - scraping and download automation
- `docs/` - mapping and data dictionary templates

## Quick Start
1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Build initial mining queue from curated sources (with connectivity probe):
   ```bash
   python3 scripts/start_data_mining.py
   ```
3. Scrape downloadable file links from seed pages:
   ```bash
   python scripts/scrape_census_links.py --seed-url https://censusindia.gov.in/
   ```
4. Download discovered files:
   ```bash
   python scripts/download_census_files.py --links-file data/raw/census2011/discovered_links.csv
   ```
5. Run the local SQLite demo pipeline (loads sample CSVs and executes transforms):
   ```bash
   python3 scripts/run_sqlite_pipeline.py
   ```
6. Create warehouse tables using SQL DDL files in `sql/ddl/` for your target DB.
7. Load real staged data and run transform SQL in `sql/transforms/`.

## Notes
- Prefer **official code-based joins** over name-based joins.
- Keep all original downloads immutable under `data/raw/`.
- Boundary changes after 2011 should be handled in a separate crosswalk table.
