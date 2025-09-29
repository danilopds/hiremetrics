{{
  config(
    materialized='incremental',
    unique_key='job_publisher_key'
  )
}}

with stg_jobs as (
    SELECT *, ROW_NUMBER() OVER ( partition by job_publisher ) name_row
    from {{ ref('stg_jobs') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['stg_jobs.job_publisher']) }} as job_publisher_key,
    False as is_job_platform,
    stg_jobs.job_publisher,
    regexp_replace(stg_jobs.job_apply_link, '^(https?://[^/]+/).*$', '\1') as job_apply_link,
    --audit columns
    stg_jobs.created_at,
    now() AS updated_at,
    stg_jobs.created_by,
    'dim_publisher_transform' AS updated_by
from stg_jobs
where stg_jobs.name_row = 1

{% if is_incremental() %}

and stg_jobs.job_publisher not in (select job_publisher from {{ this }})

{% endif %}