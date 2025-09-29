with job_skills_exploded as (
    select *           
    from {{ ref('job_skills_exploded') }}    
)

select 
    search_position_key,
    search_position_query,
    job_posted_at_date, 
    skill, 
    seniority,
    count(skill) as skill_count,
    --audit columns
    now() AS created_at,
    now() AS updated_at,
    'job_skills' AS created_by,
    'job_skills' AS updated_by
from job_skills_exploded 
group by search_position_key, search_position_query, job_posted_at_date, skill, seniority
