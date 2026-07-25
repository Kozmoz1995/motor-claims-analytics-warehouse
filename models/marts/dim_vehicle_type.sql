select
    {{ dbt_utils.generate_surrogate_key(['vehicle_type', 'vehicle_make', 'vehicle_model']) }}
        as vehicle_type_key,
    vehicle_type,
    vehicle_make,
    vehicle_model
from (
    select distinct vehicle_type, vehicle_make, vehicle_model
    from {{ ref('stg_vehicles') }}
) types
