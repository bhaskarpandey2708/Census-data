-- Upsert from stg_population_core into fact_population_2011 (SQLite/Postgres compatible pattern)

update fact_population_2011
set total_population = (
        select s.total_population from stg_population_core s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    male_population = (
        select s.male_population from stg_population_core s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    female_population = (
        select s.female_population from stg_population_core s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    source_dataset = 'pca_core',
    source_file = (
        select s.source_file from stg_population_core s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    source_sheet = (
        select s.source_sheet from stg_population_core s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    load_timestamp = current_timestamp
where exists (
    select 1 from stg_population_core s
    where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
);

insert into fact_population_2011 (
    geo_level, geo_code, census_year,
    total_population, male_population, female_population,
    source_dataset, source_file, source_sheet
)
select
    s.geo_level, s.geo_code, 2011,
    s.total_population, s.male_population, s.female_population,
    'pca_core', s.source_file, s.source_sheet
from stg_population_core s
where not exists (
    select 1 from fact_population_2011 f
    where f.geo_level = s.geo_level and f.geo_code = s.geo_code and f.census_year = 2011
);
