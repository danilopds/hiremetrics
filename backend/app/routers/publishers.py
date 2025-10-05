"""Publisher analytics endpoints

This module contains all publisher-related analytics endpoints including:
- Publisher KPIs
- Top publishers by volume
- Publisher seniority distribution
- Publisher-company matrix
- Publishers timeline
- Direct vs indirect application distribution
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..database import get_db
from ..utils.cache import cache_result
from ..utils.query_builder import SecureQueryBuilder

router = APIRouter()


@router.get("/publishers-kpis")
def get_publishers_kpis(
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """
    Get KPIs for publishers: total publishers, avg per job, biggest coverage, % direct applications.
    """
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

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        # Total unique publishers
        total_publishers_base_query = """
            WITH publishers_extracted AS (
                SELECT DISTINCT (jsonb_array_elements(apply_options::jsonb) ->> 'publisher') as publisher
                FROM target.job_dashboard_base
                {where_clause}
            )
            SELECT COUNT(*) as total_publishers
            FROM publishers_extracted
            {publisher_filter}
        """
        publisher_filter = (
            "WHERE publisher = :publisher"
            if publisher not in (None, "", "null")
            else ""
        )
        total_publishers_query = text(
            total_publishers_base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        # Average publishers per job
        avg_publishers_base_query = """
            SELECT 
                AVG(jsonb_array_length(apply_options::jsonb)) as avg_publishers_per_job
            FROM target.job_dashboard_base
            {where_clause}
        """
        avg_publishers_query = text(
            avg_publishers_base_query.format(where_clause=where_clause)
        )

        # Publisher with biggest coverage (filtered by publisher if specified)
        biggest_coverage_base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    jsonb_array_elements(apply_options::jsonb) ->> 'publisher' as publisher
                FROM target.job_dashboard_base
                {where_clause}
            ),
            publisher_coverage AS (
                SELECT 
                    publisher,
                    COUNT(DISTINCT job_id) as job_count
                FROM expanded_options
                {publisher_filter}
                GROUP BY publisher
            )
            SELECT publisher, job_count
            FROM publisher_coverage
            ORDER BY job_count DESC
            LIMIT 1
        """
        biggest_coverage_query = text(
            biggest_coverage_base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        # Percentage of direct applications
        direct_percentage_base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    jsonb_array_elements(apply_options::jsonb) as option
                FROM target.job_dashboard_base
                {where_clause}
            ),
            {filtered_options_cte}
            direct_stats AS (
                SELECT 
                    job_id,
                    BOOL_OR((option ->> 'is_direct')::boolean) as has_direct
                FROM {source_table}
                GROUP BY job_id
            )
            SELECT 
                CASE 
                    WHEN COUNT(*) = 0 THEN 0
                    ELSE ROUND(
                        (COUNT(*) FILTER (WHERE has_direct = true) * 100.0 / COUNT(*)), 2
                    )
                END as direct_percentage
            FROM direct_stats
        """

        if publisher not in (None, "", "null"):
            filtered_options_cte = "filtered_options AS (SELECT job_id, option FROM expanded_options WHERE option ->> 'publisher' = :publisher),"
            source_table = "filtered_options"
        else:
            filtered_options_cte = ""
            source_table = "expanded_options"

        direct_percentage_query = text(
            direct_percentage_base_query.format(
                where_clause=where_clause,
                filtered_options_cte=filtered_options_cte,
                source_table=source_table,
            )
        )

        total_publishers_result = db.execute(total_publishers_query, params).fetchone()
        avg_publishers_result = db.execute(avg_publishers_query, params).fetchone()
        biggest_coverage_result = db.execute(biggest_coverage_query, params).fetchone()
        direct_percentage_result = db.execute(
            direct_percentage_query, params
        ).fetchone()

        return {
            "total_publishers": (
                total_publishers_result[0] if total_publishers_result else 0
            ),
            "avg_publishers_per_job": (
                round(float(avg_publishers_result[0] or 0), 2)
                if avg_publishers_result
                else 0
            ),
            "biggest_coverage_publisher": (
                biggest_coverage_result[0] if biggest_coverage_result else None
            ),
            "biggest_coverage_count": (
                biggest_coverage_result[1] if biggest_coverage_result else 0
            ),
            "direct_percentage": (
                float(direct_percentage_result[0] or 0)
                if direct_percentage_result
                else 0
            ),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/top-publishers")
@cache_result(ttl=300, key_prefix="top_publishers")  # Cache for 5 minutes
def get_top_publishers(
    limit: int = Query(20, ge=1, le=100),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get top publishers by volume of publications."""
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

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    jsonb_array_elements(apply_options::jsonb) ->> 'publisher' as publisher
                FROM target.job_dashboard_base
                {where_clause}
            )
            SELECT 
                publisher,
                COUNT(*) as publication_count,
                COUNT(DISTINCT job_id) as unique_jobs_count
            FROM expanded_options
            {publisher_filter}
            GROUP BY publisher
            ORDER BY unique_jobs_count DESC
            LIMIT :limit
        """
        publisher_filter = (
            "WHERE publisher = :publisher"
            if publisher not in (None, "", "null")
            else ""
        )
        query = text(
            base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        result = db.execute(query, params)
        publishers = result.mappings().all()
        return publishers

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/publishers-seniority-distribution")
def get_publishers_seniority_distribution(
    limit: int = Query(10, ge=1, le=50),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get seniority distribution by top publishers."""
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

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    jsonb_array_elements(apply_options::jsonb) ->> 'publisher' as publisher
                FROM target.job_dashboard_base
                {where_clause}
            ),
            top_publishers AS (
                SELECT 
                    publisher,
                    COUNT(*) as total_count
                FROM expanded_options
                {publisher_filter}
                GROUP BY publisher
                ORDER BY total_count DESC
                LIMIT :limit
            ),
            publisher_seniority AS (
                SELECT DISTINCT
                    eo.publisher,
                    jdb.seniority,
                    eo.job_id
                FROM expanded_options eo
                INNER JOIN target.job_dashboard_base jdb ON eo.job_id = jdb.job_id
                INNER JOIN top_publishers tp ON eo.publisher = tp.publisher
            )
            SELECT 
                publisher,
                seniority,
                COUNT(job_id) as job_count
            FROM publisher_seniority
            WHERE seniority IS NOT NULL
            GROUP BY publisher, seniority
            ORDER BY publisher, seniority DESC
        """
        publisher_filter = (
            "WHERE publisher = :publisher"
            if publisher not in (None, "", "null")
            else ""
        )
        query = text(
            base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        result = db.execute(query, params)
        distribution = result.mappings().all()
        return distribution

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/publishers-companies-matrix")
def get_publishers_companies_matrix(
    limit_publishers: int = Query(15, ge=5, le=50),
    limit_companies: int = Query(15, ge=5, le=50),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get publisher × company usage matrix."""
    try:
        # Validate and sanitize inputs
        validated_limit_publishers = SecureQueryBuilder.validate_integer_input(
            limit_publishers, "limit_publishers", 5, 50
        )
        validated_limit_companies = SecureQueryBuilder.validate_integer_input(
            limit_companies, "limit_companies", 5, 50
        )

        # Build secure filters
        filters = []
        params = {
            "limit_publishers": validated_limit_publishers,
            "limit_companies": validated_limit_companies,
        }

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

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        # Optimized query with better structure and reduced CTEs
        base_query = """
            WITH publisher_counts AS (
                SELECT 
                    jsonb_array_elements(apply_options::jsonb) ->> 'publisher' as publisher,
                    COUNT(*) as total_count
                FROM target.job_dashboard_base
                {where_clause}
                AND apply_options IS NOT NULL
                AND apply_options::jsonb != '[]'::jsonb
                {publisher_filter}
                GROUP BY jsonb_array_elements(apply_options::jsonb) ->> 'publisher'
                ORDER BY total_count DESC
                LIMIT :limit_publishers
            ),
            company_counts AS (
                SELECT 
                    employer_name,
                    COUNT(*) as total_count
                FROM target.job_dashboard_base
                {where_clause}
                GROUP BY employer_name
                ORDER BY total_count DESC
                LIMIT :limit_companies
            ),
            matrix_data AS (
                SELECT 
                    jsonb_array_elements(jdb.apply_options::jsonb) ->> 'publisher' as publisher,
                    jdb.employer_name,
                    jdb.job_id
                FROM target.job_dashboard_base jdb
                INNER JOIN company_counts cc ON jdb.employer_name = cc.employer_name
                {where_clause}
                AND jdb.apply_options IS NOT NULL
                AND jdb.apply_options::jsonb != '[]'::jsonb
            )
            SELECT 
                md.publisher,
                md.employer_name,
                COUNT(md.job_id) as job_count
            FROM matrix_data md
            INNER JOIN publisher_counts pc ON md.publisher = pc.publisher
            GROUP BY md.publisher, md.employer_name
            ORDER BY md.publisher, md.employer_name
        """
        publisher_filter = (
            "WHERE publisher = :publisher"
            if publisher not in (None, "", "null")
            else ""
        )
        query = text(
            base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        result = db.execute(query, params)
        matrix = result.mappings().all()
        return matrix

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/publishers-timeline")
def get_publishers_timeline(
    limit: int = Query(10, ge=1, le=20),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get publishers timeline data."""
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

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    job_posted_at_date,
                    jsonb_array_elements(apply_options::jsonb) ->> 'publisher' as publisher
                FROM target.job_dashboard_base
                {where_clause}
            ),
            top_publishers AS (
                SELECT 
                    publisher,
                    COUNT(*) as total_count
                FROM expanded_options
                {publisher_filter}
                GROUP BY publisher
                ORDER BY total_count DESC
                LIMIT :limit
            ),
            publisher_timeline AS (
                SELECT DISTINCT
                    eo.job_posted_at_date,
                    eo.publisher,
                    eo.job_id
                FROM expanded_options eo
                INNER JOIN top_publishers tp ON eo.publisher = tp.publisher
            )
            SELECT 
                job_posted_at_date,
                publisher,
                COUNT(job_id) as job_count
            FROM publisher_timeline
            GROUP BY job_posted_at_date, publisher
            ORDER BY job_posted_at_date, publisher
        """
        publisher_filter = (
            "WHERE publisher = :publisher"
            if publisher not in (None, "", "null")
            else ""
        )
        query = text(
            base_query.format(
                where_clause=where_clause, publisher_filter=publisher_filter
            )
        )

        result = db.execute(query, params)
        timeline = result.mappings().all()
        return timeline

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/direct-vs-indirect-distribution")
def get_direct_vs_indirect_distribution(
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    publisher: Optional[str] = Query(None, description="Filter by publisher"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get direct vs indirect application distribution."""
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

        # Validate publisher input if provided
        if publisher not in (None, "", "null"):
            validated_publisher = SecureQueryBuilder.validate_text_input(
                publisher, "publisher"
            )
            params["publisher"] = validated_publisher

        base_query = """
            WITH expanded_options AS (
                SELECT 
                    job_id,
                    jsonb_array_elements(apply_options::jsonb) as option
                FROM target.job_dashboard_base
                {where_clause}
            ),
            {filtered_options_cte}
            application_types AS (
                SELECT 
                    (option ->> 'is_direct')::boolean as is_direct,
                    COUNT(*) as count
                FROM {source_table}
                GROUP BY is_direct
            )
            SELECT 
                CASE WHEN is_direct THEN 'Direct' ELSE 'Indirect' END as application_type,
                count,
                ROUND(count * 100.0 / SUM(count) OVER (), 2) as percentage
            FROM application_types
            ORDER BY is_direct DESC
        """

        if publisher not in (None, "", "null"):
            filtered_options_cte = "filtered_options AS (SELECT job_id, option FROM expanded_options WHERE option ->> 'publisher' = :publisher),"
            source_table = "filtered_options"
        else:
            filtered_options_cte = ""
            source_table = "expanded_options"

        query = text(
            base_query.format(
                where_clause=where_clause,
                filtered_options_cte=filtered_options_cte,
                source_table=source_table,
            )
        )

        result = db.execute(query, params)
        distribution = result.mappings().all()
        return distribution

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
