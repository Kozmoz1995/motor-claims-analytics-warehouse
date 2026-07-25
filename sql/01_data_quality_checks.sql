-- 01 | DATA QUALITY AND RECONCILIATION
-- Run after dbt build. Every query should return zero rows or a zero count.

-- Duplicate collision natural keys.
select collision_id, count(*) as duplicate_count
from marts.fact_collision
group by collision_id
having count(*) > 1;

-- Invalid casualty totals.
select collision_id, persons_injured, persons_killed
from marts.fact_collision
where persons_injured < 0 or persons_killed < 0;

-- Orphan vehicle facts.
select count(*) as orphan_vehicle_rows
from marts.fact_vehicle_involvement v
left join marts.fact_collision c on c.collision_key = v.collision_key
where c.collision_key is null;

-- Reconcile fact grain with source grain.
select
    (select count(*) from staging.stg_crashes) as source_rows,
    (select count(*) from marts.fact_collision) as fact_rows,
    (select count(*) from staging.stg_crashes)
      - (select count(*) from marts.fact_collision) as difference;

-- Missing geocodes by borough.
select
    l.borough,
    count(*) as collisions,
    count(*) filter (
        where l.latitude is null or l.longitude is null
    ) as missing_geocode,
    round(
        count(*) filter (
            where l.latitude is null or l.longitude is null
        )::numeric / nullif(count(*), 0),
        4
    ) as missing_geocode_rate
from marts.fact_collision f
join marts.dim_location l on l.location_key = f.location_key
group by l.borough
order by missing_geocode_rate desc;

