-- 06 | POWER BI SERVING CONTRACT
-- dbt owns the reporting views. These queries document the BI contract and
-- make validation straightforward for analysts using PostgreSQL directly.

select * from reporting.rpt_collision_overview;
select * from reporting.rpt_vehicle_risk;
select * from reporting.rpt_hotspot;
select * from reporting.rpt_fraud_signal_proxy;

-- Recommended indexes when equivalent tables are materialized.
-- create unique index on reporting.rpt_collision_overview (collision_key);
-- create index on reporting.rpt_collision_overview (crash_date, borough);
-- create index on reporting.rpt_collision_overview (risk_segment);
-- create index on reporting.rpt_fraud_signal_proxy (review_status);

