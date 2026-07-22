{{ config(materialized='table') }}

with bounds as (
    select min(crash_date) as min_date, max(crash_date) as max_date
    from {{ ref('stg_crashes') }}
),
dates as (
    select generate_series(min_date, max_date, interval '1 day')::date as full_date
    from bounds
)
select
    to_char(full_date, 'YYYYMMDD')::integer as date_key,
    full_date,
    extract(year from full_date)::smallint as year_number,
    extract(quarter from full_date)::smallint as quarter_number,
    extract(month from full_date)::smallint as month_number,
    trim(to_char(full_date, 'Month')) as month_name,
    extract(isodow from full_date)::smallint as iso_day_of_week,
    trim(to_char(full_date, 'Day')) as day_name,
    (extract(isodow from full_date) in (6, 7)) as is_weekend
from dates
