-- Upsert from stg_religion

update fact_population_2011
set religion_hindu_population = (
        select s.religion_hindu_population from stg_religion s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    religion_muslim_population = (
        select s.religion_muslim_population from stg_religion s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    source_dataset = coalesce(source_dataset, 'religion'),
    source_file = (
        select s.source_file from stg_religion s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    source_sheet = (
        select s.source_sheet from stg_religion s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    load_timestamp = current_timestamp
where exists (
    select 1 from stg_religion s
    where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
);

insert into fact_population_2011 (
    geo_level, geo_code, census_year,
    religion_hindu_population, religion_muslim_population,
    source_dataset, source_file, source_sheet
)
select
    s.geo_level, s.geo_code, 2011,
    s.religion_hindu_population, s.religion_muslim_population,
    'religion', s.source_file, s.source_sheet
from stg_religion s
where not exists (
    select 1 from fact_population_2011 f
    where f.geo_level = s.geo_level and f.geo_code = s.geo_code and f.census_year = 2011
);
