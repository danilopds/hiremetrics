{{
  config(
    materialized='incremental',
    unique_key='job_id'
  )
}}

with stg_jobs as (
    select *
    from {{ ref('stg_jobs') }}
),

final as (
    select
        {{ dbt_utils.generate_surrogate_key(['stg_jobs.employer_name']) }} as employer_key,
        {{ dbt_utils.generate_surrogate_key(['stg_jobs.job_location']) }} as location_key,
        {{ dbt_utils.generate_surrogate_key(['stg_jobs.job_publisher']) }} as publisher_key,
        stg_jobs.job_id,
        stg_jobs.job_title,        
        stg_jobs.job_employment_type,
        stg_jobs.job_employment_types,
        stg_jobs.job_apply_link,
        stg_jobs.job_apply_is_direct,
        stg_jobs.apply_options,
        stg_jobs.job_description,
        stg_jobs.job_is_remote,
        stg_jobs.job_posted_at,
        stg_jobs.job_posted_at_datetime_utc,
        stg_jobs.job_benefits,
        stg_jobs.job_google_link,
        stg_jobs.job_salary,
        stg_jobs.job_min_salary,
        stg_jobs.job_max_salary,
        stg_jobs.job_salary_period,
        stg_jobs.job_highlights,
        stg_jobs.job_onet_soc,
        stg_jobs.job_onet_job_zone,
        stg_jobs.extracted_skills,
        stg_jobs.seniority,
        stg_jobs.search_position_key,
        stg_jobs.search_position_query,
        --audit columns
        stg_jobs.created_at,
        now() AS updated_at,
        stg_jobs.created_by,
        'fact_jobs_transform' AS updated_by
    from stg_jobs

    {% if is_incremental() %}
    where stg_jobs.updated_at > (select max(updated_at) from {{ this }})
    {% endif %}
)

select * from final