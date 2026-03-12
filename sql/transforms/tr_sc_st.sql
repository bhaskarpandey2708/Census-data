-- Upsert from stg_sc_st

update fact_population_2011
set sc_population = (
        select s.sc_population from stg_sc_st s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    st_population = (
        select s.st_population from stg_sc_st s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    source_dataset = coalesce(source_dataset, 'sc_st'),
    source_file = (
        select s.source_file from stg_sc_st s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    source_sheet = (
        select s.source_sheet from stg_sc_st s
        where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
    ),
    load_timestamp = current_timestamp
where exists (
    select 1 from stg_sc_st s
    where s.geo_level = fact_population_2011.geo_level and s.geo_code = fact_population_2011.geo_code
);

insert into fact_population_2011 (
    geo_level, geo_code, census_year,
    sc_population, st_population,
    source_dataset, source_file, source_sheet
)
select
    s.geo_level, s.geo_code, 2011,
    s.sc_population, s.st_population,
    'sc_st', s.source_file, s.source_sheet
from stg_sc_st s
where not exists (
    select 1 from fact_population_2011 f
    where f.geo_level = s.geo_level and f.geo_code = s.geo_code and f.census_year = 2011
);
