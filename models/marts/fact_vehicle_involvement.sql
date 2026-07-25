select
    v.vehicle_involvement_id as vehicle_involvement_key,
    v.vehicle_involvement_id,
    v.collision_id as collision_key,
    to_char(v.crash_date, 'YYYYMMDD')::integer as crash_date_key,
    d.vehicle_type_key,
    v.vehicle_year,
    v.travel_direction,
    v.pre_crash_action,
    v.primary_factor,
    1::integer as vehicle_count,
    v.ingested_at
from {{ ref('stg_vehicles') }} v
join {{ ref('dim_vehicle_type') }} d
  on v.vehicle_type = d.vehicle_type
 and v.vehicle_make = d.vehicle_make
 and v.vehicle_model = d.vehicle_model
