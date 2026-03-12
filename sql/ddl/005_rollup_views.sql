create view if not exists vw_state_population_2011 as
select
    v.state_code,
    sum(f.total_population) as total_population,
    sum(f.male_population) as male_population,
    sum(f.female_population) as female_population,
    sum(f.sc_population) as sc_population,
    sum(f.st_population) as st_population,
    sum(f.rural_population) as rural_population,
    sum(f.urban_population) as urban_population,
    sum(f.religion_hindu_population) as religion_hindu_population,
    sum(f.religion_muslim_population) as religion_muslim_population
from fact_population_2011 f
join dim_village v on f.geo_level = 'village' and f.geo_code = v.village_code
group by v.state_code;
