{{ config(materialized='view') }}

with vehicle_metrics as (
    select
        v.vehicle_type,
        count(*) as vehicle_involvements,
        count(distinct f.collision_key) as collisions,
        sum(f.is_severe::integer) as severe_collisions,
        sum(f.persons_injured) as persons_injured,
        sum(f.persons_killed) as persons_killed,
        avg(
            f.persons_injured
            + 5 * f.persons_killed
            + 2 * f.pedestrians_injured
            + 2 * f.cyclists_injured
        )::numeric as avg_severity_score
    from {{ ref('fact_vehicle_involvement') }} vi
    join {{ ref('dim_vehicle_type') }} v
      on v.vehicle_type_key = vi.vehicle_type_key
    join {{ ref('fact_collision') }} f
      on f.collision_key = vi.collision_key
    group by v.vehicle_type
)
select
    *,
    round(severe_collisions::numeric / nullif(collisions, 0), 4)
        as severe_collision_rate,
    dense_rank() over (order by avg_severity_score desc) as severity_rank,
    ntile(4) over (order by avg_severity_score) as risk_quartile
from vehicle_metrics

