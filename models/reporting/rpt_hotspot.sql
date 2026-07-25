{{ config(materialized='view') }}

with location_metrics as (
    select
        l.borough,
        l.zip_code,
        l.on_street_name,
        l.cross_street_name,
        l.latitude,
        l.longitude,
        count(*) as collisions,
        sum(f.is_severe::integer) as severe_collisions,
        sum(f.persons_injured) as persons_injured,
        sum(f.persons_killed) as persons_killed
    from {{ ref('fact_collision') }} f
    join {{ ref('dim_location') }} l on l.location_key = f.location_key
    group by
        l.borough, l.zip_code, l.on_street_name, l.cross_street_name,
        l.latitude, l.longitude
)
select
    *,
    round(severe_collisions::numeric / nullif(collisions, 0), 4)
        as severe_collision_rate,
    dense_rank() over (
        partition by borough
        order by collisions desc, severe_collisions desc
    ) as borough_hotspot_rank
from location_metrics

