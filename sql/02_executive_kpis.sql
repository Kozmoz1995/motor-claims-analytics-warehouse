-- 02 | EXECUTIVE KPI LAYER

select
    count(*) as total_collisions,
    sum(persons_injured) as persons_injured,
    sum(persons_killed) as persons_killed,
    sum(is_severe::integer) as severe_collisions,
    round(avg(is_severe::integer), 4) as severe_collision_rate,
    round(avg(
        persons_injured + 5 * persons_killed
        + 2 * pedestrians_injured + 2 * cyclists_injured
    ), 2) as avg_severity_score
from marts.fact_collision;

-- Year-over-year comparison.
with annual as (
    select
        d.year_number,
        count(*) as collisions,
        sum(f.is_severe::integer) as severe_collisions
    from marts.fact_collision f
    join marts.dim_date d on d.date_key = f.crash_date_key
    group by d.year_number
)
select
    *,
    lag(collisions) over (order by year_number) as prior_year_collisions,
    round(
        100.0 * (
            collisions - lag(collisions) over (order by year_number)
        ) / nullif(lag(collisions) over (order by year_number), 0),
        2
    ) as collision_yoy_pct
from annual
order by year_number;

