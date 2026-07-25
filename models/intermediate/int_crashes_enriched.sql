select
    *,
    case
        when persons_killed > 0 then 'Fatal'
        when persons_injured >= 3 then 'Severe injury'
        when persons_injured > 0 then 'Injury'
        else 'Property damage only'
    end as severity_band,
    (persons_killed > 0 or persons_injured >= 3) as is_severe
from {{ ref('stg_crashes') }}
