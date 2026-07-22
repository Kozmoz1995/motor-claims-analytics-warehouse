select
    unique_id::bigint as person_involvement_id,
    collision_id::bigint as collision_id,
    crash_date::date as crash_date,
    coalesce(nullif(trim(person_type), ''), 'Unknown') as person_role,
    coalesce(nullif(trim(person_injury), ''), 'Unknown') as injury_status,
    nullif(trim(person_age), '')::integer as person_age,
    coalesce(nullif(trim(person_sex), ''), 'U') as person_sex,
    coalesce(nullif(trim(safety_equipment), ''), 'Unknown') as safety_equipment,
    _ingested_at::timestamptz as ingested_at
from {{ source('raw', 'persons') }}
