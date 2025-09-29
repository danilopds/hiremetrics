-- Table: target.job_skills

-- DROP TABLE IF EXISTS target.job_skills;

CREATE TABLE IF NOT EXISTS target.job_skills
(
    search_position_key text COLLATE pg_catalog."default",
    search_position_query text COLLATE pg_catalog."default",
    job_posted_at_date timestamp without time zone,
    skill text COLLATE pg_catalog."default",
    seniority text COLLATE pg_catalog."default",
    skill_count bigint,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    created_by text COLLATE pg_catalog."default",
    updated_by text COLLATE pg_catalog."default"
)