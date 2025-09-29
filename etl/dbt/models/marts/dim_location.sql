{{
  config(
    materialized='incremental',
    unique_key='location_key'
  )
}}

with stg_jobs as (
    SELECT *, ROW_NUMBER() OVER ( partition by job_location ) name_row
    from {{ ref('stg_jobs') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['stg_jobs.job_location']) }} as location_key,
    stg_jobs.job_location,
    stg_jobs.job_city,
    stg_jobs.job_state,
    stg_jobs.job_country,
    stg_jobs.job_latitude,
    stg_jobs.job_longitude,
    --audit columns
    stg_jobs.created_at,
    now() AS updated_at,
    stg_jobs.created_by,
    'dim_location_transform' AS updated_by
from stg_jobs
where stg_jobs.name_row = 1

{% if is_incremental() %}

and stg_jobs.updated_at > (select max(updated_at) from {{ this }})

{% endif %}