-- Table: target.job_dashboard_base

-- DROP TABLE IF EXISTS target.job_dashboard_base;

CREATE TABLE IF NOT EXISTS target.job_dashboard_base
(
    search_position_key text COLLATE pg_catalog."default",
    search_position_query text COLLATE pg_catalog."default",
    job_id text COLLATE pg_catalog."default",
    job_title text COLLATE pg_catalog."default",
    job_employment_type text COLLATE pg_catalog."default",
    job_is_remote boolean,    
    job_posted_at_date timestamp without time zone,
    job_publisher text COLLATE pg_catalog."default",
    extracted_skills text COLLATE pg_catalog."default",
    seniority text COLLATE pg_catalog."default",
    apply_options text COLLATE pg_catalog."default",
    employer_name text COLLATE pg_catalog."default",
    job_city text COLLATE pg_catalog."default",
    job_state text COLLATE pg_catalog."default",
    is_job_platform boolean,
    created_at timestamp without time zone,
    updated_at timestamp with time zone,
    created_by text COLLATE pg_catalog."default",
    updated_by text COLLATE pg_catalog."default"
)