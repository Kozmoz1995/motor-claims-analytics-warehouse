select
    unique_id::bigint as vehicle_involvement_id,
    collision_id::bigint as collision_id,
    crash_date::date as crash_date,
    coalesce(nullif(trim(vehicle_type), ''), 'Unknown') as vehicle_type,
    coalesce(nullif(trim(vehicle_make), ''), 'Unknown') as vehicle_make,
    coalesce(nullif(trim(vehicle_model), ''), 'Unknown') as vehicle_model,
    nullif(trim(vehicle_year), '')::integer as vehicle_year,
    coalesce(nullif(trim(travel_direction), ''), 'Unknown') as travel_direction,
    coalesce(nullif(trim(pre_crash), ''), 'Unknown') as pre_crash_action,
    coalesce(nullif(trim(contributing_factor_1), ''), 'Unknown') as primary_factor,
    _ingested_at::timestamptz as ingested_at
from {{ source('raw', 'vehicles') }}
