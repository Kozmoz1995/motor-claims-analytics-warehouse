with locations as (
    select distinct
        coalesce(borough, 'Unknown') as borough,
        coalesce(zip_code, 'Unknown') as zip_code,
        coalesce(on_street_name, 'Unknown') as on_street_name,
        coalesce(cross_street_name, 'Unknown') as cross_street_name,
        latitude,
        longitude
    from {{ ref('stg_crashes') }}
)
select
    {{ dbt_utils.generate_surrogate_key([
        'borough', 'zip_code', 'on_street_name', 'cross_street_name',
        "coalesce(latitude::text, '')", "coalesce(longitude::text, '')"
    ]) }} as location_key,
    borough,
    zip_code,
    on_street_name,
    cross_street_name,
    latitude,
    longitude,
    'New York City'::text as city,
    'New York'::text as state,
    'US'::text as country_code
from locations
