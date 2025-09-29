-- Diagnostic: Analyze duplicate job records
-- Description: Show duplicate jobs and their counts before removal
-- Date: 2025-01-27

-- Show duplicate job_ids and their counts
SELECT 
    job_id,
    COUNT(*) as duplicate_count,
    MIN(created_at) as earliest_created,
    MAX(created_at) as latest_created,
    STRING_AGG(DISTINCT job_city, ', ') as cities,
    STRING_AGG(DISTINCT job_publisher, ', ') as publishers
FROM job_dashboard_base
GROUP BY job_id
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, latest_created DESC
LIMIT 20;

-- Show total counts
SELECT 
    'Total records' as metric,
    COUNT(*) as count
FROM job_dashboard_base
UNION ALL
SELECT 
    'Unique job_ids' as metric,
    COUNT(DISTINCT job_id) as count
FROM job_dashboard_base
UNION ALL
SELECT 
    'Duplicate job_ids' as metric,
    COUNT(*) - COUNT(DISTINCT job_id) as count
FROM job_dashboard_base;

-- Show sample of duplicate records for the first few job_ids
WITH duplicate_jobs AS (
    SELECT job_id
    FROM job_dashboard_base
    GROUP BY job_id
    HAVING COUNT(*) > 1
    LIMIT 5
)
SELECT 
    j.job_id,
    j.job_title,
    j.employer_name,
    j.job_city,
    j.job_publisher,
    j.created_at,
    j.updated_at
FROM job_dashboard_base j
INNER JOIN duplicate_jobs d ON j.job_id = d.job_id
ORDER BY j.job_id, j.created_at DESC; 