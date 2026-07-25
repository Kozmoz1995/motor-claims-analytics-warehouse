{{ config(materialized='view') }}

select
    f.collision_key,
    d.full_date as crash_date,
    d.year_number,
    d.quarter_number,
    d.month_number,
    d.month_name,
    d.day_name,
    d.is_weekend,
    f.crash_time_key,
    (f.crash_time_key < 600 or f.crash_time_key >= 2200) as is_night,
    l.borough,
    l.zip_code,
    l.on_street_name,
    l.cross_street_name,
    l.latitude,
    l.longitude,
    f.primary_factor,
    f.severity_band,
    f.is_severe,
    f.collision_count,
    f.persons_injured,
    f.persons_killed,
    f.pedestrians_injured,
    f.pedestrians_killed,
    f.cyclists_injured,
    f.cyclists_killed,
    f.motorists_injured,
    f.motorists_killed,
    (
        f.persons_injured
        + 5 * f.persons_killed
        + 2 * f.pedestrians_injured
        + 2 * f.cyclists_injured
    )::numeric as severity_score,
    case
        when f.persons_killed > 0 then 'Critical'
        when f.persons_injured >= 3 then 'High'
        when f.persons_injured > 0 then 'Medium'
        else 'Low'
    end as risk_segment
from {{ ref('fact_collision') }} f
join {{ ref('dim_date') }} d on d.date_key = f.crash_date_key
join {{ ref('dim_location') }} l on l.location_key = f.location_key

