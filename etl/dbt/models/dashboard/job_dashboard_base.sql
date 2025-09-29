{{ config(materialized='view') }}

select
    fct.search_position_key,
    fct.search_position_query,
    fct.job_id,
    fct.job_title,
    fct.job_employment_type,        
    fct.job_is_remote,    
    cast(fct.job_posted_at_datetime_utc as date) as job_posted_at_date,    
    fct.extracted_skills,
    fct.seniority,
    fct.apply_options,
    --dim columns
    emp.employer_name,
    loc.job_city,
    loc.job_state,
    pub.job_publisher,
    pub.is_job_platform,
    --audit columns
    fct.created_at,
    now() AS updated_at,
    fct.created_by,
    'job_dashboard_base' AS updated_by
from {{ ref('fct_jobs_post') }} fct
left join {{ ref('dim_location') }} loc on fct.location_key = loc.location_key 
left join {{ ref('dim_employer') }} emp on fct.employer_key = emp.employer_key
left join {{ ref('dim_publisher') }} pub on fct.publisher_key = pub.job_publisher_key
--where try_cast(fct.job_posted_at_datetime_utc as timestamp) >= current_timestamp - INTERVAL 30 DAY