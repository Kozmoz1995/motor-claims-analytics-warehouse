-- 03 | SEVERITY AND VEHICLE RISK

-- Vehicle ranking, benchmark and quartile segmentation.
with vehicle_metrics as (
    select
        d.vehicle_type,
        count(*) as involvements,
        count(distinct c.collision_key) as collisions,
        sum(c.is_severe::integer) as severe_collisions,
        avg(
            c.persons_injured + 5 * c.persons_killed
            + 2 * c.pedestrians_injured + 2 * c.cyclists_injured
        ) as avg_severity_score
    from marts.fact_vehicle_involvement v
    join marts.dim_vehicle_type d
      on d.vehicle_type_key = v.vehicle_type_key
    join marts.fact_collision c on c.collision_key = v.collision_key
    group by d.vehicle_type
    having count(*) >= 100
)
select
    *,
    round(severe_collisions::numeric / nullif(collisions, 0), 4)
        as severe_collision_rate,
    dense_rank() over (order by avg_severity_score desc) as severity_rank,
    ntile(4) over (order by avg_severity_score) as risk_quartile
from vehicle_metrics
order by severity_rank;

-- Extreme severity events using a population percentile.
with scored as (
    select
        collision_id,
        persons_injured + 5 * persons_killed
          + 2 * pedestrians_injured + 2 * cyclists_injured
            as severity_score
    from marts.fact_collision
),
threshold as (
    select percentile_cont(0.95) within group (order by severity_score)
        as p95_severity
    from scored
)
select s.*, t.p95_severity
from scored s
cross join threshold t
where s.severity_score >= t.p95_severity
order by s.severity_score desc;

