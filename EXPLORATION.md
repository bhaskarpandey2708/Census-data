# Repository Exploration and Execution Update

## Previous state
- Repository started almost empty with only `.gitkeep`.

## Implemented foundation
1. Folder bootstrap for raw/staging/curated data zones.
2. SQL DDL for geography dimensions and `fact_population_2011`.
3. SQL transform templates for population core, SC/ST, rural/urban, and religion merges.
4. Quality-check SQL for consistency validation.
5. Python scripts for link scraping and file downloading.
6. Documentation: README, data dictionary, and mapping template.

## New "start data mining/scraping" implementation
1. Added curated source registry at `config/source_registry.csv`.
2. Added `scripts/start_data_mining.py` to assemble a mining queue from registry + discovered links.
3. Added URL validation and connectivity probing to produce actionable status (`ok`/`warn`).
4. Persisted output manifest at `data/raw/census2011/manifests/mining_queue.csv`.
5. Kept scraping/downloading scripts in place for the next live run when network permits.

## Immediate next execution steps
1. Re-run `scripts/start_data_mining.py` and `scripts/scrape_census_links.py` in an environment with outbound web access.
2. Download files from successful queue records into `data/raw/census2011/downloads/`.
3. Classify downloads into `pca`, `sc_st`, `religion`, and `geo_directory`.
4. Load staging tables and run transforms + QA.
