{{
  config(
    materialized='incremental',
    unique_key='job_id'
  )
}}

with fct_jobs_post as (
    select *           
    from {{ ref('fct_jobs_post') }}  
    where extracted_skills is not null  
),

exploded as (
    select
        search_position_key,
        search_position_query,
        job_id,
        cast(job_posted_at_datetime_utc as date) as job_posted_at_date,
        unnest(extracted_skills) as skill,
        seniority,
    from fct_jobs_post    

    {% if is_incremental() %}
    where fct_jobs_post.updated_at > (select max(updated_at) from {{ this }})
    {% endif %}
)

select 
    search_position_key,
    search_position_query,
    job_id,
    job_posted_at_date, 
    skill,     
    seniority,
    --audit columns
    now() AS created_at,
    now() AS updated_at,
    'job_skills_exploded' AS created_by,
    'job_skills_exploded' AS updated_by
from exploded

