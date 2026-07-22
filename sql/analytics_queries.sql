-- Monthly collision severity trend.
select
    d.year_number,
    d.month_number,
    sum(f.collision_count) as collisions,
    sum(f.persons_injured) as injured,
    sum(f.persons_killed) as killed,
    round(1000.0 * sum(f.persons_injured) / nullif(sum(f.collision_count), 0), 2)
        as injuries_per_1000_collisions
from marts.fact_collision f
join marts.dim_date d on d.date_key = f.crash_date_key
group by d.year_number, d.month_number
order by d.year_number, d.month_number;

-- Borough risk proxy. This is association, not fault or insurance pricing.
select
    l.borough,
    count(*) as collisions,
    sum(f.is_severe::integer) as severe_collisions,
    round(avg(f.is_severe::integer), 4) as severe_collision_rate
from marts.fact_collision f
join marts.dim_location l on l.location_key = f.location_key
group by l.borough
order by severe_collision_rate desc;

-- Vehicle types most often involved in severe collisions.
select
    v.vehicle_type,
    count(*) as vehicle_involvements,
    sum(c.is_severe::integer) as severe_involvements,
    round(avg(c.is_severe::integer), 4) as severe_involvement_rate
from marts.fact_vehicle_involvement f
join marts.dim_vehicle_type v on v.vehicle_type_key = f.vehicle_type_key
join marts.fact_collision c on c.collision_key = f.collision_key
group by v.vehicle_type
having count(*) >= 100
order by severe_involvement_rate desc;
