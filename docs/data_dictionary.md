# Data Dictionary (Starter)

## `fact_population_2011`
- `geo_level`: state | district | block | gp | village
- `geo_code`: official code for selected geography level
- `census_year`: fixed to 2011
- `total_population`: total persons
- `male_population`: male persons
- `female_population`: female persons
- `sc_population`: scheduled caste population
- `st_population`: scheduled tribe population
- `rural_population`: rural population
- `urban_population`: urban population
- `religion_hindu_population`: hindu population
- `religion_muslim_population`: muslim population
- `source_dataset`: pca_core | sc_st | rural_urban | religion
- `source_file`: original file name
- `source_sheet`: sheet/tab name in source
- `load_timestamp`: ingestion timestamp

## Geography hierarchy
- `dim_state`
- `dim_district`
- `dim_block`
- `dim_gram_panchayat`
- `dim_village`
