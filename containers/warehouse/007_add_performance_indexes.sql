-- Add performance indexes for job_dashboard_base and job_skills tables
-- Migration: 8_add_performance_indexes.sql

-- Enable pg_trgm extension for text search optimization
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Indexes for job_dashboard_base table
CREATE INDEX IF NOT EXISTS idx_job_dashboard_date ON target.job_dashboard_base(job_posted_at_date);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_employer ON target.job_dashboard_base(employer_name);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_publisher ON target.job_dashboard_base(job_publisher);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_remote ON target.job_dashboard_base(job_is_remote);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_seniority ON target.job_dashboard_base(seniority);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_position ON target.job_dashboard_base(search_position_query);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_city ON target.job_dashboard_base(job_city);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_state ON target.job_dashboard_base(job_state);

-- Trigram indexes for ILIKE operations
CREATE INDEX IF NOT EXISTS idx_job_dashboard_city_trgm ON target.job_dashboard_base USING GIN (job_city gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_state_trgm ON target.job_dashboard_base USING GIN (job_state gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_employer_trgm ON target.job_dashboard_base USING GIN (employer_name gin_trgm_ops);

-- JSONB indexes for extracted_skills and apply_options
CREATE INDEX IF NOT EXISTS idx_job_dashboard_skills_gin ON target.job_dashboard_base USING GIN ((extracted_skills::jsonb));
CREATE INDEX IF NOT EXISTS idx_job_dashboard_apply_options_gin ON target.job_dashboard_base USING GIN ((apply_options::jsonb));

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_job_dashboard_date_employer ON target.job_dashboard_base(job_posted_at_date, employer_name);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_date_publisher ON target.job_dashboard_base(job_posted_at_date, job_publisher);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_date_remote ON target.job_dashboard_base(job_posted_at_date, job_is_remote);
CREATE INDEX IF NOT EXISTS idx_job_dashboard_date_seniority ON target.job_dashboard_base(job_posted_at_date, seniority);

-- Indexes for job_skills table
CREATE INDEX IF NOT EXISTS idx_job_skills_date ON target.job_skills(job_posted_at_date);
CREATE INDEX IF NOT EXISTS idx_job_skills_skill ON target.job_skills(skill);
CREATE INDEX IF NOT EXISTS idx_job_skills_seniority ON target.job_skills(seniority);
CREATE INDEX IF NOT EXISTS idx_job_skills_position ON target.job_skills(search_position_query);

-- Composite indexes for job_skills
CREATE INDEX IF NOT EXISTS idx_job_skills_date_skill ON target.job_skills(job_posted_at_date, skill);
CREATE INDEX IF NOT EXISTS idx_job_skills_date_seniority ON target.job_skills(job_posted_at_date, seniority);
CREATE INDEX IF NOT EXISTS idx_job_skills_skill_seniority ON target.job_skills(skill, seniority);

-- Add comments for documentation
COMMENT ON INDEX target.idx_job_dashboard_date IS 'Index for filtering by job posted date';
COMMENT ON INDEX target.idx_job_dashboard_employer IS 'Index for filtering by employer name';
COMMENT ON INDEX target.idx_job_dashboard_publisher IS 'Index for filtering by job publisher';
COMMENT ON INDEX target.idx_job_dashboard_remote IS 'Index for filtering by remote status';
COMMENT ON INDEX target.idx_job_dashboard_seniority IS 'Index for filtering by seniority level';
COMMENT ON INDEX target.idx_job_dashboard_position IS 'Index for filtering by position query';
COMMENT ON INDEX target.idx_job_dashboard_city IS 'Index for filtering by job city';
COMMENT ON INDEX target.idx_job_dashboard_state IS 'Index for filtering by job state';
COMMENT ON INDEX target.idx_job_dashboard_skills_gin IS 'GIN index for JSONB skills array operations';
COMMENT ON INDEX target.idx_job_dashboard_apply_options_gin IS 'GIN index for JSONB apply options operations'; 