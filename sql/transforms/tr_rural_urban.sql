-- Upsert from stg_rural_urban

update fact_population_2011
set rural_population = (
        select s.rural_population from stg_rural_urban s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    urban_population = (
        select s.urban_population from stg_rural_urban s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    source_dataset = coalesce(source_dataset, 'rural_urban'),
    source_file = (
        select s.source_file from stg_rural_urban s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    source_sheet = (
        select s.source_sheet from stg_rural_urban s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    load_timestamp = current_timestamp
where exists (
    select 1 from stg_rural_urban s
    where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
);

insert into fact_population_2011 (
    geo_level, geo_code, census_year,
    rural_population, urban_population,
    source_dataset, source_file, source_sheet
)
select
    s.geo_level, s.geo_code, 2011,
    s.rural_population, s.urban_population,
    'rural_urban', s.source_file, s.source_sheet
from stg_rural_urban s
where not exists (
    select 1 from fact_population_2011 f
    where f.geo_level = s.geo_level and f.geo_code = s.geo_code and f.census_year = 2011
);
