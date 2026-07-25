{{ config(materialized='view') }}

with collision_context as (
    select
        o.*,
        count(vi.vehicle_involvement_key) as vehicle_count
    from {{ ref('rpt_collision_overview') }} o
    left join {{ ref('fact_vehicle_involvement') }} vi
      on vi.collision_key = o.collision_key
    group by
        o.collision_key, o.crash_date, o.year_number, o.quarter_number,
        o.month_number, o.month_name, o.day_name, o.is_weekend,
        o.crash_time_key, o.is_night, o.borough, o.zip_code,
        o.on_street_name, o.cross_street_name, o.latitude, o.longitude,
        o.primary_factor, o.severity_band, o.is_severe, o.collision_count,
        o.persons_injured, o.persons_killed, o.pedestrians_injured,
        o.pedestrians_killed, o.cyclists_injured, o.cyclists_killed,
        o.motorists_injured, o.motorists_killed, o.severity_score,
        o.risk_segment
)
select
    *,
    (
        case when is_night then 15 else 0 end
        + case when vehicle_count >= 3 then 20 else 0 end
        + case when latitude is null or longitude is null then 20 else 0 end
        + case when primary_factor = 'Unspecified' then 15 else 0 end
        + case when persons_injured >= 4 then 20 else 0 end
        + case when is_weekend then 10 else 0 end
    )::integer as anomaly_signal_score,
    case
        when (
            case when is_night then 15 else 0 end
            + case when vehicle_count >= 3 then 20 else 0 end
            + case when latitude is null or longitude is null then 20 else 0 end
            + case when primary_factor = 'Unspecified' then 15 else 0 end
            + case when persons_injured >= 4 then 20 else 0 end
            + case when is_weekend then 10 else 0 end
        ) >= 40 then 'Review'
        else 'Standard'
    end as review_status
from collision_context

