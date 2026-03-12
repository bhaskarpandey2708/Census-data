-- male + female should equal total where all three are present
select *
from fact_population_2011
where total_population is not null
  and male_population is not null
  and female_population is not null
  and total_population <> male_population + female_population;

-- rural + urban should equal total where present
select *
from fact_population_2011
where total_population is not null
  and rural_population is not null
  and urban_population is not null
  and total_population <> rural_population + urban_population;

-- SC/ST should not exceed total population
select *
from fact_population_2011
where (sc_population is not null and total_population is not null and sc_population > total_population)
   or (st_population is not null and total_population is not null and st_population > total_population);
