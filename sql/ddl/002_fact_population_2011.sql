create table if not exists fact_population_2011 (
    geo_level varchar(20) not null,
    geo_code varchar(25) not null,
    census_year int not null default 2011,

    total_population bigint,
    male_population bigint,
    female_population bigint,

    sc_population bigint,
    st_population bigint,

    rural_population bigint,
    urban_population bigint,

    religion_hindu_population bigint,
    religion_muslim_population bigint,

    source_dataset varchar(100),
    source_file varchar(255),
    source_sheet varchar(255),
    load_timestamp timestamp default current_timestamp,

    primary key (geo_level, geo_code, census_year)
);
