select
    c.collision_id as collision_key,
    c.collision_id,
    to_char(c.crash_date, 'YYYYMMDD')::integer as crash_date_key,
    extract(hour from c.crash_time)::smallint * 100
        + extract(minute from c.crash_time)::smallint as crash_time_key,
    l.location_key,
    c.primary_factor,
    c.severity_band,
    c.is_severe,
    1::integer as collision_count,
    c.persons_injured,
    c.persons_killed,
    c.pedestrians_injured,
    c.pedestrians_killed,
    c.cyclists_injured,
    c.cyclists_killed,
    c.motorists_injured,
    c.motorists_killed,
    c.ingested_at
from {{ ref('int_crashes_enriched') }} c
join {{ ref('dim_location') }} l
  on coalesce(c.borough, 'Unknown') = l.borough
 and coalesce(c.zip_code, 'Unknown') = l.zip_code
 and coalesce(c.on_street_name, 'Unknown') = l.on_street_name
 and coalesce(c.cross_street_name, 'Unknown') = l.cross_street_name
 and c.latitude is not distinct from l.latitude
 and c.longitude is not distinct from l.longitude
