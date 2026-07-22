select
    p.person_involvement_id as person_involvement_key,
    p.person_involvement_id,
    p.collision_id as collision_key,
    to_char(p.crash_date, 'YYYYMMDD')::integer as crash_date_key,
    r.person_role_key,
    p.person_age,
    p.person_sex,
    p.safety_equipment,
    p.injury_status,
    (upper(p.injury_status) = 'INJURED')::integer as is_injured,
    (upper(p.injury_status) = 'KILLED')::integer as is_killed,
    1::integer as person_count,
    p.ingested_at
from {{ ref('stg_persons') }} p
join {{ ref('dim_person_role') }} r using (person_role)
