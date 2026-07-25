-- 05 | HOTSPOTS AND SEASONALITY

-- Top five hotspots inside every borough.
select *
from reporting.rpt_hotspot
where borough_hotspot_rank <= 5
order by borough, borough_hotspot_rank;

-- Rolling 30-day collision and severity trend.
with daily as (
    select
        crash_date,
        count(*) as collisions,
        sum(is_severe::integer) as severe_collisions
    from reporting.rpt_collision_overview
    group by crash_date
)
select
    *,
    round(avg(collisions) over (
        order by crash_date
        rows between 29 preceding and current row
    ), 2) as collision_30d_avg,
    round(avg(severe_collisions) over (
        order by crash_date
        rows between 29 preceding and current row
    ), 2) as severe_30d_avg
from daily
order by crash_date;

-- Hour and weekday risk matrix.
select
    day_name,
    crash_time_key / 100 as crash_hour,
    count(*) as collisions,
    sum(is_severe::integer) as severe_collisions,
    round(avg(is_severe::integer), 4) as severe_collision_rate
from reporting.rpt_collision_overview
group by day_name, crash_time_key / 100
order by day_name, crash_hour;

