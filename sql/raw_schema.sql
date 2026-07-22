create schema if not exists raw;

create table if not exists raw.crashes (
    collision_id bigint primary key,
    crash_date timestamp,
    crash_time text,
    borough text,
    zip_code text,
    latitude numeric,
    longitude numeric,
    on_street_name text,
    cross_street_name text,
    number_of_persons_injured integer,
    number_of_persons_killed integer,
    number_of_pedestrians_injured integer,
    number_of_pedestrians_killed integer,
    number_of_cyclist_injured integer,
    number_of_cyclist_killed integer,
    number_of_motorist_injured integer,
    number_of_motorist_killed integer,
    contributing_factor_vehicle_1 text,
    _ingested_at timestamptz not null default now()
);

create table if not exists raw.vehicles (
    unique_id bigint primary key,
    collision_id bigint not null,
    crash_date timestamp,
    vehicle_type text,
    vehicle_make text,
    vehicle_model text,
    vehicle_year text,
    travel_direction text,
    pre_crash text,
    contributing_factor_1 text,
    _ingested_at timestamptz not null default now()
);

create table if not exists raw.persons (
    unique_id bigint primary key,
    collision_id bigint not null,
    crash_date timestamp,
    person_type text,
    person_injury text,
    person_age text,
    person_sex text,
    safety_equipment text,
    _ingested_at timestamptz not null default now()
);
