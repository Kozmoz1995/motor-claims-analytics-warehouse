-- 04 | EXPLAINABLE ANOMALY SIGNALS
-- These are review indicators, not fraud labels or accusations.

select
    review_status,
    count(*) as collisions,
    round(avg(anomaly_signal_score), 2) as avg_signal_score,
    sum(persons_injured) as persons_injured,
    sum(persons_killed) as persons_killed
from reporting.rpt_fraud_signal_proxy
group by review_status
order by collisions desc;

-- Explain which indicators contribute most to review volume.
select
    count(*) filter (where is_night) as night_events,
    count(*) filter (where vehicle_count >= 3) as multi_vehicle_events,
    count(*) filter (
        where latitude is null or longitude is null
    ) as missing_location_events,
    count(*) filter (
        where primary_factor = 'Unspecified'
    ) as unspecified_factor_events,
    count(*) filter (where persons_injured >= 4)
        as high_injury_events
from reporting.rpt_fraud_signal_proxy
where review_status = 'Review';

