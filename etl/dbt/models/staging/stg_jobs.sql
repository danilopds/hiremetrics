with source as (
    select * from {{ source('source', 'jobs') }} t1 
    inner join {{ source('source', 'jobs_skills') }} t2 on t1.job_id = t2.job_id
),

data_fixes as (
    select
        *,
        -- Fill missing locations
        coalesce(job_city, 'Brasil (N/A)') as calculated_job_city,
        coalesce(job_state, 'Brasil (N/A)') as calculated_job_state,
        coalesce(job_location, 'Brasil (N/A)') as calculated_job_location,
        -- Fill missing employment types
        case
            when job_employment_type is null then 'Tempo integral'
            else job_employment_type
        end as calculated_job_employment_type,
        -- Amended employer names
        case
            when employer_name = 'Caderno Nacional' then job_publisher
            else employer_name
        end as calculated_employer_name,
        -- normalize employer_website: strip the protocol, trim spaces, strip trailing '/', lowercase
        lower(rtrim(trim(regexp_replace(employer_website, '^https?://', '')), '/')) as calculated_employer_website,
        -- Cast timestamp fields to proper type
        try_cast(created_at as timestamp) as created_at_tmst,
        -- Fill missing timestamps with comprehensive time pattern matching
        case
            when job_posted_at is null then created_at_tmst
            when job_posted_at like '%minutos%' then 
                created_at_tmst - interval '1 minute' * cast(regexp_replace(job_posted_at, '[^0-9]', '', 'g') as integer)
            when job_posted_at like '%hora%' and job_posted_at not like '%horas%' then 
                created_at_tmst - interval '1 hour' * cast(regexp_replace(job_posted_at, '[^0-9]', '', 'g') as integer)
            when job_posted_at like '%horas%' then 
                created_at_tmst - interval '1 hour' * cast(regexp_replace(job_posted_at, '[^0-9]', '', 'g') as integer)
            when job_posted_at like '%dia%' and job_posted_at not like '%dias%' then 
                created_at_tmst - interval '1 day' * cast(regexp_replace(job_posted_at, '[^0-9]', '', 'g') as integer)
            when job_posted_at like '%dias%' then 
                created_at_tmst - interval '1 day' * cast(regexp_replace(job_posted_at, '[^0-9]', '', 'g') as integer)
            when job_posted_at like '%mês%' or job_posted_at like '%meses%' then 
                created_at_tmst - interval '1 month' * cast(regexp_replace(job_posted_at, '[^0-9]', '', 'g') as integer)
            else created_at_tmst
        end as calculated_timestamp
    from source
),

staged as (
    select
        data_fixes.job_id,
        data_fixes.job_title,
        data_fixes.calculated_employer_name as employer_name,
        data_fixes.employer_logo,
        data_fixes.calculated_employer_website as employer_website,
        data_fixes.job_publisher,
        data_fixes.calculated_job_employment_type as job_employment_type,
        data_fixes.job_employment_types,
        data_fixes.job_apply_link,
        data_fixes.job_apply_is_direct,
        data_fixes.apply_options,
        data_fixes.job_description,
        data_fixes.job_is_remote,        
        data_fixes.job_posted_at,
        data_fixes.calculated_timestamp as job_posted_at_timestamp,
        data_fixes.calculated_timestamp as job_posted_at_datetime_utc,        
        data_fixes.calculated_job_city as job_city,
        data_fixes.calculated_job_state as job_state,
        data_fixes.calculated_job_location as job_location,        
        data_fixes.job_country,
        data_fixes.job_latitude,
        data_fixes.job_longitude,
        data_fixes.job_benefits,
        data_fixes.job_google_link,
        data_fixes.job_salary,
        data_fixes.job_min_salary,
        data_fixes.job_max_salary,
        data_fixes.job_salary_period,
        data_fixes.job_highlights,
        data_fixes.job_onet_soc,
        data_fixes.job_onet_job_zone,
        data_fixes.extracted_skills,
        data_fixes.seniority,        
        data_fixes.search_position_key,
        data_fixes.search_position_query,
        data_fixes.created_at_tmst as created_at,
        now() AS updated_at,
        data_fixes.created_by,
        'stg_jobs' AS updated_by
    from data_fixes
)

select * from staged 