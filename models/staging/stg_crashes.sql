with source as (
    select * from {{ source('raw', 'crashes') }}
),
renamed as (
    select
        collision_id::bigint as collision_id,
        crash_date::date as crash_date,
        crash_time::time as crash_time,
        nullif(trim(borough), '') as borough,
        nullif(trim(zip_code), '') as zip_code,
        latitude::numeric(9,6) as latitude,
        longitude::numeric(9,6) as longitude,
        nullif(initcap(trim(on_street_name)), '') as on_street_name,
        nullif(initcap(trim(cross_street_name)), '') as cross_street_name,
        coalesce(number_of_persons_injured, 0)::integer as persons_injured,
        coalesce(number_of_persons_killed, 0)::integer as persons_killed,
        coalesce(number_of_pedestrians_injured, 0)::integer as pedestrians_injured,
        coalesce(number_of_pedestrians_killed, 0)::integer as pedestrians_killed,
        coalesce(number_of_cyclist_injured, 0)::integer as cyclists_injured,
        coalesce(number_of_cyclist_killed, 0)::integer as cyclists_killed,
        coalesce(number_of_motorist_injured, 0)::integer as motorists_injured,
        coalesce(number_of_motorist_killed, 0)::integer as motorists_killed,
        coalesce(nullif(trim(contributing_factor_vehicle_1), ''), 'Unknown') as primary_factor,
        _ingested_at::timestamptz as ingested_at
    from source
)
select * from renamed
