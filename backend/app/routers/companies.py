"""Company analytics endpoints

This module contains all company-related analytics endpoints including:
- Top companies by job count
- Company seniority distribution
- Employment type distribution
- Remote job percentages
- Company job timelines
- Top skills by company
- Company KPIs
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.query_service import get_job_platforms
from ..utils.cache import cache_result
from ..utils.query_builder import SecureQueryBuilder

router = APIRouter()


@router.get("/top-companies")
@cache_result(ttl=300, key_prefix="top_companies")  # Cache for 5 minutes
def get_top_companies(
    limit: int = Query(20, ge=1, le=100),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get top companies by job count."""
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 100
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Use JOIN approach for job platform exclusion
        if job_platforms:
            # Create a CTE for job platforms to exclude
            platform_cte = """
            WITH job_platforms_to_exclude AS (
                SELECT DISTINCT job_publisher as platform_name
                FROM target.job_dashboard_base
                WHERE is_job_platform = true
                AND job_publisher IS NOT NULL
                AND job_publisher != ''
            )
            SELECT 
                jdb.employer_name,
                COUNT(jdb.job_id) as job_count
            FROM target.job_dashboard_base jdb
            LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
            {where_clause}
            AND jpe.platform_name IS NULL
            GROUP BY jdb.employer_name
            ORDER BY job_count DESC
            LIMIT :limit
            """
            full_query = platform_cte.format(where_clause=where_clause)
        else:
            # No job platforms to exclude, use simple approach
            base_query = """
                SELECT 
                    employer_name,
                    COUNT(job_id) as job_count
                FROM target.job_dashboard_base
                {where_clause}
                GROUP BY employer_name
                ORDER BY job_count DESC
                LIMIT :limit
            """
            full_query = base_query.format(where_clause=where_clause)

        query = text(full_query)
        result = db.execute(query, params)
        companies = result.mappings().all()
        return companies

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/companies-seniority-distribution")
def get_companies_seniority_distribution(
    limit: int = Query(10, ge=1, le=50),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get seniority distribution by top companies."""
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 50
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # If filtering by a specific company, simplify the query
        if employer_name not in (None, "", "null"):
            # Build additional filters excluding employer_name
            additional_filters = [
                f for f in filters if not f.startswith("employer_name")
            ]
            additional_where = (
                f"AND {' AND '.join(additional_filters)}" if additional_filters else ""
            )

            base_query = """
                SELECT 
                    employer_name,
                    seniority,
                    COUNT(job_id) as job_count
                FROM target.job_dashboard_base
                WHERE employer_name = :employer_name
                {additional_where}
                GROUP BY employer_name, seniority
                ORDER BY employer_name, seniority DESC
            """
            full_query = base_query.format(additional_where=additional_where)
        else:
            # Build WHERE clause for the main query
            main_where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

            # Use LEFT JOIN to exclude job platforms
            if job_platforms:
                # Create a CTE for job platforms to exclude
                platform_cte = """
                WITH job_platforms_to_exclude AS (
                    SELECT DISTINCT job_publisher as platform_name
                    FROM target.job_dashboard_base
                    WHERE is_job_platform = true
                    AND job_publisher IS NOT NULL
                    AND job_publisher != ''
                ),
                top_companies AS (
                    SELECT jdb.employer_name
                    FROM target.job_dashboard_base jdb
                    LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                    {main_where_clause}
                    AND jpe.platform_name IS NULL
                    GROUP BY jdb.employer_name
                    ORDER BY COUNT(jdb.job_id) DESC
                    LIMIT :limit
                )
                SELECT 
                    jdb.employer_name,
                    jdb.seniority,
                    COUNT(jdb.job_id) as job_count
                FROM target.job_dashboard_base jdb
                INNER JOIN top_companies tc ON jdb.employer_name = tc.employer_name
                LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                {main_where_clause}
                AND jpe.platform_name IS NULL
                GROUP BY jdb.employer_name, jdb.seniority
                ORDER BY jdb.employer_name, jdb.seniority DESC
                """
                full_query = platform_cte.format(main_where_clause=main_where_clause)
            else:
                # No job platforms to exclude, use simple approach
                base_query = """
                WITH top_companies AS (
                    SELECT employer_name
                    FROM target.job_dashboard_base
                    {main_where_clause}
                    GROUP BY employer_name
                    ORDER BY COUNT(job_id) DESC
                    LIMIT :limit
                )
                SELECT 
                    jdb.employer_name,
                    jdb.seniority,
                    COUNT(jdb.job_id) as job_count
                FROM target.job_dashboard_base jdb
                INNER JOIN top_companies tc ON jdb.employer_name = tc.employer_name
                {main_where_clause}
                GROUP BY jdb.employer_name, jdb.seniority
                ORDER BY jdb.employer_name, jdb.seniority DESC
                """
                full_query = base_query.format(main_where_clause=main_where_clause)

        try:
            query = text(full_query)
            result = db.execute(query, params)
            distribution = result.mappings().all()
            return distribution
        except Exception as e:
            raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/companies-remote-percentage")
def get_companies_remote_percentage(
    limit: int = Query(20, ge=1, le=100),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get remote job percentage by company."""
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 100
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Use JOIN approach for job platform exclusion
        if job_platforms:
            # Create a CTE for job platforms to exclude
            platform_cte = """
            WITH job_platforms_to_exclude AS (
                SELECT DISTINCT job_publisher as platform_name
                FROM target.job_dashboard_base
                WHERE is_job_platform = true
                AND job_publisher IS NOT NULL
                AND job_publisher != ''
            )
            """

            # If filtering by a specific company, job_is_remote, or seniority, don't filter by minimum job count
            if (
                employer_name not in (None, "", "null")
                or job_is_remote not in (None, "", "null")
                or seniority not in (None, "", "null")
            ):
                base_query = """
                {platform_cte}
                SELECT 
                    jdb.employer_name,
                    COUNT(jdb.job_id) as total_jobs,
                    SUM(CASE WHEN jdb.job_is_remote = true THEN 1 ELSE 0 END) as remote_jobs,
                    ROUND(
                        SUM(CASE WHEN jdb.job_is_remote = true THEN 1 ELSE 0 END) * 100.0 / COUNT(jdb.job_id), 
                        2
                    ) as remote_percentage
                FROM target.job_dashboard_base jdb
                LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                {where_clause}
                AND jpe.platform_name IS NULL
                GROUP BY jdb.employer_name
                ORDER BY remote_percentage DESC, total_jobs DESC
                LIMIT :limit
                """
                full_query = base_query.format(
                    platform_cte=platform_cte, where_clause=where_clause
                )
            else:
                # Modified logic: Show companies with remote jobs or companies with at least 2 jobs
                base_query = """
                {platform_cte}
                SELECT 
                    jdb.employer_name,
                    COUNT(jdb.job_id) as total_jobs,
                    SUM(CASE WHEN jdb.job_is_remote = true THEN 1 ELSE 0 END) as remote_jobs,
                    ROUND(
                        SUM(CASE WHEN jdb.job_is_remote = true THEN 1 ELSE 0 END) * 100.0 / COUNT(jdb.job_id), 
                        2
                    ) as remote_percentage
                FROM target.job_dashboard_base jdb
                LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                {where_clause}
                AND jpe.platform_name IS NULL
                GROUP BY jdb.employer_name
                HAVING COUNT(jdb.job_id) >= 2 OR SUM(CASE WHEN jdb.job_is_remote = true THEN 1 ELSE 0 END) > 0
                ORDER BY remote_percentage DESC, total_jobs DESC
                LIMIT :limit
                """
                full_query = base_query.format(
                    platform_cte=platform_cte, where_clause=where_clause
                )
        else:
            # No job platforms to exclude, use simple approach
            if (
                employer_name not in (None, "", "null")
                or job_is_remote not in (None, "", "null")
                or seniority not in (None, "", "null")
            ):
                base_query = """
                    SELECT 
                        employer_name,
                        COUNT(job_id) as total_jobs,
                        SUM(CASE WHEN job_is_remote = true THEN 1 ELSE 0 END) as remote_jobs,
                        ROUND(
                            SUM(CASE WHEN job_is_remote = true THEN 1 ELSE 0 END) * 100.0 / COUNT(job_id), 
                            2
                        ) as remote_percentage
                    FROM target.job_dashboard_base
                    {where_clause}
                    GROUP BY employer_name
                    ORDER BY remote_percentage DESC, total_jobs DESC
                    LIMIT :limit
                """
                full_query = base_query.format(where_clause=where_clause)
            else:
                # Modified logic: Show companies with remote jobs or companies with at least 2 jobs
                base_query = """
                    SELECT 
                        employer_name,
                        COUNT(job_id) as total_jobs,
                        SUM(CASE WHEN job_is_remote = true THEN 1 ELSE 0 END) as remote_jobs,
                        ROUND(
                            SUM(CASE WHEN job_is_remote = true THEN 1 ELSE 0 END) * 100.0 / COUNT(job_id), 
                            2
                        ) as remote_percentage
                    FROM target.job_dashboard_base
                    {where_clause}
                    GROUP BY employer_name
                    HAVING COUNT(job_id) >= 2 OR SUM(CASE WHEN job_is_remote = true THEN 1 ELSE 0 END) > 0
                    ORDER BY remote_percentage DESC, total_jobs DESC
                    LIMIT :limit
                """
                full_query = base_query.format(where_clause=where_clause)

        query = text(full_query)
        result = db.execute(query, params)
        remote_stats = result.mappings().all()
        return remote_stats

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/companies-jobs-timeline")
def get_companies_jobs_timeline(
    limit: int = Query(5, ge=1, le=20),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get jobs timeline by top companies."""
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 20
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # If filtering by a specific company, simplify the query
        if employer_name not in (None, "", "null"):
            # Build additional filters excluding employer_name
            additional_filters = [
                f for f in filters if not f.startswith("employer_name")
            ]
            additional_where = (
                f"AND {' AND '.join(additional_filters)}" if additional_filters else ""
            )

            base_query = """
                SELECT 
                    job_posted_at_date,
                    employer_name,
                    COUNT(job_id) as job_count
                FROM target.job_dashboard_base
                WHERE employer_name = :employer_name
                {additional_where}
                GROUP BY job_posted_at_date, employer_name
                ORDER BY job_posted_at_date, employer_name
            """
            full_query = base_query.format(additional_where=additional_where)
        else:
            # Build WHERE clause for the main query
            main_where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

            # Use LEFT JOIN to exclude job platforms
            if job_platforms:
                # Create a CTE for job platforms to exclude
                platform_cte = """
                WITH job_platforms_to_exclude AS (
                    SELECT DISTINCT job_publisher as platform_name
                    FROM target.job_dashboard_base
                    WHERE is_job_platform = true
                    AND job_publisher IS NOT NULL
                    AND job_publisher != ''
                ),
                top_companies AS (
                    SELECT jdb.employer_name
                    FROM target.job_dashboard_base jdb
                    LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                    {main_where_clause}
                    AND jpe.platform_name IS NULL
                    GROUP BY jdb.employer_name
                    ORDER BY COUNT(jdb.job_id) DESC
                    LIMIT :limit
                )
                SELECT 
                    jdb.job_posted_at_date,
                    jdb.employer_name,
                    COUNT(jdb.job_id) as job_count
                FROM target.job_dashboard_base jdb
                INNER JOIN top_companies tc ON jdb.employer_name = tc.employer_name
                LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                {main_where_clause}
                AND jpe.platform_name IS NULL
                GROUP BY jdb.job_posted_at_date, jdb.employer_name
                ORDER BY jdb.job_posted_at_date, jdb.employer_name
                """
                full_query = platform_cte.format(main_where_clause=main_where_clause)
            else:
                # No job platforms to exclude, use simple approach
                base_query = """
                WITH top_companies AS (
                    SELECT employer_name
                    FROM target.job_dashboard_base
                    {main_where_clause}
                    GROUP BY employer_name
                    ORDER BY COUNT(job_id) DESC
                    LIMIT :limit
                )
                SELECT 
                    jdb.job_posted_at_date,
                    jdb.employer_name,
                    COUNT(jdb.job_id) as job_count
                FROM target.job_dashboard_base jdb
                INNER JOIN top_companies tc ON jdb.employer_name = tc.employer_name
                {main_where_clause}
                GROUP BY jdb.job_posted_at_date, jdb.employer_name
                ORDER BY jdb.job_posted_at_date, jdb.employer_name
                """
                full_query = base_query.format(main_where_clause=main_where_clause)

        try:
            query = text(full_query)
            result = db.execute(query, params)
            timeline = result.mappings().all()
            return timeline
        except Exception as e:
            raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/companies-top-skills")
def get_companies_top_skills(
    limit: int = Query(10, ge=1, le=50),
    skills_limit: int = Query(10, ge=5, le=50),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get top skills by company with word cloud format data."""
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 50
        )
        validated_skills_limit = SecureQueryBuilder.validate_integer_input(
            skills_limit, "skills_limit", 5, 50
        )

        # Build secure filters
        filters = []
        params = {"limit": validated_limit, "skills_limit": validated_skills_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # If filtering by a specific company, simplify the query
        if employer_name not in (None, "", "null"):
            # Build additional filters excluding employer_name
            additional_filters = [
                f for f in filters if not f.startswith("employer_name")
            ]
            additional_where = (
                f"AND {' AND '.join(additional_filters)}" if additional_filters else ""
            )

            base_query = """
                WITH skills_extracted AS (
                    SELECT 
                        jsonb_array_elements_text(extracted_skills::jsonb) as skill
                    FROM target.job_dashboard_base
                    WHERE employer_name = :employer_name
                    AND extracted_skills IS NOT NULL
                    AND extracted_skills::jsonb != '[]'::jsonb
                    {additional_where}
                )
                SELECT 
                    skill as name,
                    COUNT(*) as value
                FROM skills_extracted
                GROUP BY skill
                ORDER BY value DESC
                LIMIT :skills_limit
            """
            full_query = base_query.format(additional_where=additional_where)
        else:
            # For all companies or filtered subset - optimized version
            base_query = """
                WITH company_skills AS (
                    SELECT 
                        jsonb_array_elements_text(extracted_skills::jsonb) as skill
                    FROM target.job_dashboard_base
                    {where_clause}
                    AND extracted_skills IS NOT NULL
                    AND extracted_skills::jsonb != '[]'::jsonb
                    AND employer_name IN (
                        SELECT employer_name
                        FROM target.job_dashboard_base
                        {where_clause}
                        GROUP BY employer_name
                        ORDER BY COUNT(*) DESC
                        LIMIT :limit
                    )
                )
                SELECT 
                    skill as name,
                    COUNT(*) as value
                FROM company_skills
                GROUP BY skill
                ORDER BY value DESC
                LIMIT :skills_limit
            """
            full_query = base_query.format(where_clause=where_clause)

        query = text(full_query)
        result = db.execute(query, params)
        skills = result.mappings().all()
        return list(skills)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/companies-kpis")
def get_companies_kpis(
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get KPIs for companies: total job postings, % remote jobs, average skills per job."""
    try:
        # Build secure filters
        filters = []
        params = {}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            if validated_remote is True:
                filters.append("job_is_remote = true")
            elif validated_remote is False:
                filters.append("job_is_remote = false")

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Total job postings
        total_jobs_base_query = """
            SELECT COUNT(DISTINCT job_id) as total_jobs
            FROM target.job_dashboard_base
            {where_clause}
        """
        total_jobs_query = text(total_jobs_base_query.format(where_clause=where_clause))

        # Percentage of remote jobs
        remote_percentage_base_query = """
            SELECT 
                ROUND(
                    (COUNT(DISTINCT job_id) FILTER (WHERE job_is_remote = true) * 100.0 / 
                     NULLIF(COUNT(DISTINCT job_id), 0)), 2
                ) as remote_percentage
            FROM target.job_dashboard_base
            {where_clause}
        """
        remote_percentage_query = text(
            remote_percentage_base_query.format(where_clause=where_clause)
        )

        # Average skills per job
        avg_skills_base_query = """
            SELECT 
                ROUND(AVG(skills_per_job), 2) as avg_skills_per_job
            FROM (
                SELECT 
                    job_id,
                    COALESCE(jsonb_array_length(extracted_skills::jsonb), 0) as skills_per_job
                FROM target.job_dashboard_base
                WHERE extracted_skills IS NOT NULL
                {additional_where}
            ) job_skill_counts
        """
        additional_where = f"AND {' AND '.join(filters)}" if filters else ""
        avg_skills_query = text(
            avg_skills_base_query.format(additional_where=additional_where)
        )

        # Count of distinct companies
        distinct_companies_base_query = """
            SELECT COUNT(DISTINCT employer_name) as distinct_companies
            FROM target.job_dashboard_base
            WHERE employer_name IS NOT NULL
            {additional_where}
        """
        distinct_companies_query = text(
            distinct_companies_base_query.format(additional_where=additional_where)
        )

        total_jobs_result = db.execute(total_jobs_query, params).fetchone()
        remote_percentage_result = db.execute(
            remote_percentage_query, params
        ).fetchone()
        avg_skills_result = db.execute(avg_skills_query, params).fetchone()
        distinct_companies_result = db.execute(
            distinct_companies_query, params
        ).fetchone()

        return {
            "total_jobs": total_jobs_result[0] if total_jobs_result else 0,
            "remote_percentage": (
                float(remote_percentage_result[0] or 0)
                if remote_percentage_result
                else 0
            ),
            "avg_skills_per_job": (
                float(avg_skills_result[0] or 0) if avg_skills_result else 0
            ),
            "distinct_companies": (
                distinct_companies_result[0] if distinct_companies_result else 0
            ),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
