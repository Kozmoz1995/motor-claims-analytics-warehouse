-- Learning alternative to the denormalized location star dimension.
create schema if not exists snowflake_mart;

create table if not exists snowflake_mart.dim_state (
    state_key integer generated always as identity primary key,
    state_name varchar(100) not null unique,
    country_code char(2) not null
);

create table if not exists snowflake_mart.dim_city (
    city_key integer generated always as identity primary key,
    state_key integer not null references snowflake_mart.dim_state,
    city_name varchar(100) not null,
    unique (state_key, city_name)
);

create table if not exists snowflake_mart.dim_borough (
    borough_key integer generated always as identity primary key,
    city_key integer not null references snowflake_mart.dim_city,
    borough_name varchar(100) not null,
    unique (city_key, borough_name)
);

create table if not exists snowflake_mart.dim_location (
    location_key bigint generated always as identity primary key,
    borough_key integer not null references snowflake_mart.dim_borough,
    zip_code varchar(12),
    on_street_name text,
    cross_street_name text,
    latitude numeric(9,6),
    longitude numeric(9,6)
);

-- In the production star model city/state/borough live directly in dim_location.
-- In this alternative, fact_collision joins location, then traverses the hierarchy.
