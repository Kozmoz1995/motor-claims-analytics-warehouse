select
    row_number() over (order by person_role)::integer as person_role_key,
    person_role
from (select distinct person_role from {{ ref('stg_persons') }}) roles
