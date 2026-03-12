create table if not exists stg_population_core (
    geo_level text not null,
    geo_code text not null,
    total_population integer,
    male_population integer,
    female_population integer,
    source_file text,
    source_sheet text
);

create table if not exists stg_sc_st (
    geo_level text not null,
    geo_code text not null,
    sc_population integer,
    st_population integer,
    source_file text,
    source_sheet text
);

create table if not exists stg_rural_urban (
    geo_level text not null,
    geo_code text not null,
    rural_population integer,
    urban_population integer,
    source_file text,
    source_sheet text
);

create table if not exists stg_religion (
    geo_level text not null,
    geo_code text not null,
    religion_hindu_population integer,
    religion_muslim_population integer,
    source_file text,
    source_sheet text
);
