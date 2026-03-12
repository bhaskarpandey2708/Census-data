create table if not exists dim_state (
    state_code varchar(10) primary key,
    state_name varchar(150) not null,
    census_year int not null default 2011
);

create table if not exists dim_district (
    district_code varchar(15) primary key,
    district_name varchar(150) not null,
    state_code varchar(10) not null references dim_state(state_code),
    census_year int not null default 2011
);

create table if not exists dim_block (
    block_code varchar(20) primary key,
    block_name varchar(150) not null,
    district_code varchar(15) not null references dim_district(district_code),
    census_year int not null default 2011
);

create table if not exists dim_gram_panchayat (
    gp_code varchar(25) primary key,
    gp_name varchar(150) not null,
    block_code varchar(20) not null references dim_block(block_code),
    census_year int not null default 2011
);

create table if not exists dim_village (
    village_code varchar(25) primary key,
    village_name varchar(200) not null,
    gp_code varchar(25) references dim_gram_panchayat(gp_code),
    block_code varchar(20) not null references dim_block(block_code),
    district_code varchar(15) not null references dim_district(district_code),
    state_code varchar(10) not null references dim_state(state_code),
    is_urban boolean,
    census_year int not null default 2011
);
