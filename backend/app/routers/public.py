"""Public endpoints (no authentication required)

This module contains all public-facing endpoints that don't require authentication.
These endpoints are designed for the landing page and allow potential users to
preview data before signing up.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..schemas import CSVExportRequest, ExportCountResponse
from ..services.query_service import build_where_clause_and_params, get_job_platforms
from ..utils.query_builder import SecureQueryBuilder

router = APIRouter()


@router.get("/preview-export", response_model=list[schemas.JobExportData])
async def public_preview_export(
    job_posted_at_date_from: Optional[str] = Query(None),
    job_posted_at_date_to: Optional[str] = Query(None),
    search_position_query: Optional[str] = Query(None, description="Filter by position query"),
    employer_names: Optional[str] = Query(
        None, description="Comma-separated list of employer names"
    ),
    publishers: Optional[str] = Query(None, description="Comma-separated list of publishers"),
    seniority_levels: Optional[str] = Query(
        None, description="Comma-separated list of seniority levels"
    ),
    employment_types: Optional[str] = Query(
        None, description="Comma-separated list of employment types"
    ),
    cities: Optional[str] = Query(None, description="Comma-separated list of cities"),
    states: Optional[str] = Query(None, description="Comma-separated list of states"),
    skills: Optional[str] = Query(None, description="Comma-separated list of skills"),
    job_is_remote: Optional[bool] = Query(None),
    is_direct: Optional[bool] = Query(None),
    limit: int = Query(10, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Public endpoint for previewing export data (no authentication required).
    Used for the home page data preview section to showcase available data.
    """
    try:
        # Validate limit parameter
        validated_limit = SecureQueryBuilder.validate_integer_input(limit, "limit", 1, 1000)

        # Parse and validate comma-separated parameters
        filters = schemas.CSVExportFilters(
            job_posted_at_date_from=job_posted_at_date_from,
            job_posted_at_date_to=job_posted_at_date_to,
            search_position_query=search_position_query,
            employer_names=employer_names.split(",") if employer_names else [],
            publishers=publishers.split(",") if publishers else [],
            seniority_levels=seniority_levels.split(",") if seniority_levels else [],
            employment_types=employment_types.split(",") if employment_types else [],
            cities=cities.split(",") if cities else [],
            states=states.split(",") if states else [],
            skills=skills.split(",") if skills else [],
            job_is_remote=job_is_remote,
            is_direct=is_direct,
        )

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Build secure WHERE clause with validated filters
        where_clause, params = build_where_clause_and_params(filters)
        params["limit"] = validated_limit

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

            query = text(
                f"""
            {platform_cte}
            SELECT 
                jdb.job_id,
                jdb.job_title,
                jdb.employer_name,
                jdb.job_posted_at_date,
                jdb.job_city,
                jdb.job_state,
                jdb.seniority,
                jdb.job_employment_type,
                jdb.job_is_remote,
                jdb.job_publisher,
                jdb.extracted_skills,
                jdb.apply_options,
                jdb.search_position_query,
                jdb.created_at,
                jdb.updated_at
            FROM target.job_dashboard_base jdb
            LEFT JOIN job_platforms_to_exclude jpe ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
            {where_clause}
            AND jpe.platform_name IS NULL
            ORDER BY jdb.job_posted_at_date DESC
            LIMIT :limit
            """
            )
        else:
            query = text(
                f"""
                SELECT 
                    jdb.job_id,
                    jdb.job_title,
                    jdb.employer_name,
                    jdb.job_posted_at_date,
                    jdb.job_city,
                    jdb.job_state,
                    jdb.seniority,
                    jdb.job_employment_type,
                    jdb.job_is_remote,
                    jdb.job_publisher,
                    jdb.extracted_skills,
                    jdb.apply_options,
                    jdb.search_position_query,
                    jdb.created_at,
                    jdb.updated_at
                FROM target.job_dashboard_base jdb
                {where_clause}
                ORDER BY jdb.job_posted_at_date DESC
                LIMIT :limit
            """
            )

        result = db.execute(query, params)
        jobs = result.mappings().all()
        return jobs

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/count-export-records", response_model=ExportCountResponse)
async def public_count_export_records(request: CSVExportRequest, db: Session = Depends(get_db)):
    """
    Public endpoint for counting export records (no authentication required).
    Used for the home page data preview section to show data volume.
    """
    try:
        # Build where clause and params
        where_clause, params = build_where_clause_and_params(request.filters)

        # Count total records
        count_query = text(
            f"""
            SELECT COUNT(*) as total_records
            FROM target.job_dashboard_base jdb
            {where_clause}
        """
        )

        result = db.execute(count_query, params)
        total_records = result.scalar()

        return ExportCountResponse(count=total_records, max_allowed=request.max_records)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting records: {str(e)}")


@router.get("/available-positions", response_model=list[str])
async def public_get_available_positions(db: Session = Depends(get_db)):
    """
    Public endpoint for getting available positions (no authentication required).
    Used for the home page data preview section to populate position filters.

    Returns a limited list of the most common positions to avoid overwhelming
    unauthenticated users.
    """
    try:
        # Use parameterized query (no user input, so safe)
        # Limit to 50 positions for public access
        query = text(
            """
            SELECT DISTINCT search_position_query
            FROM target.job_dashboard_base
            WHERE search_position_query IS NOT NULL AND search_position_query != ''
            ORDER BY search_position_query
            LIMIT 50
        """
        )

        result = db.execute(query)
        positions = [row[0] for row in result]
        return positions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching positions: {str(e)}")


@router.get("/available-locations", response_model=dict)
async def public_get_available_locations(db: Session = Depends(get_db)):
    """
    Public endpoint for getting available locations (no authentication required).
    Returns cities and states for filter population on landing page.
    Limited to top 50 of each to avoid overwhelming unauthenticated users.
    """
    try:
        # Get top 50 cities
        cities_query = text(
            """
            SELECT DISTINCT job_city
            FROM target.job_dashboard_base
            WHERE job_city IS NOT NULL AND job_city != ''
            ORDER BY job_city
            LIMIT 50
        """
        )

        # Get all states (limited set anyway)
        states_query = text(
            """
            SELECT DISTINCT job_state
            FROM target.job_dashboard_base
            WHERE job_state IS NOT NULL AND job_state != ''
            ORDER BY job_state
        """
        )

        cities_result = db.execute(cities_query)
        states_result = db.execute(states_query)

        cities = [row[0] for row in cities_result]
        states = [row[0] for row in states_result]

        return {"cities": cities, "states": states}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching locations: {str(e)}")


@router.get("/available-employment-types", response_model=list[str])
async def public_get_available_employment_types(db: Session = Depends(get_db)):
    """
    Public endpoint for getting available employment types (no authentication required).
    Returns employment type options for filter population on landing page.
    """
    try:
        query = text(
            """
            SELECT DISTINCT job_employment_type
            FROM target.job_dashboard_base
            WHERE job_employment_type IS NOT NULL AND job_employment_type != ''
            ORDER BY job_employment_type
        """
        )

        result = db.execute(query)
        employment_types = [row[0] for row in result]
        return employment_types

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching employment types: {str(e)}")


@router.get("/available-skills", response_model=list[str])
async def public_get_available_skills(db: Session = Depends(get_db)):
    """
    Public endpoint for getting available skills (no authentication required).
    Returns top 100 skills for filter population on landing page.
    Limited to prevent overwhelming unauthenticated users.
    """
    try:
        # Limit to top 100 skills for public access
        query = text(
            """
            WITH skill_counts AS (
                SELECT 
                    skill,
                    COUNT(*) as count
                FROM target.job_dashboard_base,
                     LATERAL jsonb_array_elements_text(extracted_skills::jsonb) as skill
                WHERE extracted_skills IS NOT NULL 
                    AND extracted_skills::text != 'null'
                    AND extracted_skills::text != '[]'
                GROUP BY skill
                ORDER BY count DESC
                LIMIT 100
            )
            SELECT skill
            FROM skill_counts
            ORDER BY skill
        """
        )

        result = db.execute(query)
        skills = [row[0] for row in result]
        return skills

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching skills: {str(e)}")


@router.get("/available-seniority-levels", response_model=list[str])
async def public_get_available_seniority_levels(db: Session = Depends(get_db)):
    """
    Public endpoint for getting available seniority levels (no authentication required).
    Returns seniority levels for filter population on landing page.
    """
    try:
        query = text(
            """
            SELECT DISTINCT seniority
            FROM target.job_dashboard_base
            WHERE seniority IS NOT NULL AND seniority != ''
            ORDER BY seniority
        """
        )

        result = db.execute(query)
        seniority_levels = [row[0] for row in result]
        return seniority_levels

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching seniority levels: {str(e)}")


@router.get("/available-companies", response_model=list[str])
async def public_get_available_companies(db: Session = Depends(get_db)):
    """
    Public endpoint for getting available companies (no authentication required).
    Returns top 100 companies for filter population on landing page.
    Limited to prevent overwhelming unauthenticated users and excludes job platforms.
    """
    try:
        # Get job platforms to exclude
        job_platforms = get_job_platforms(db)

        if job_platforms:
            # Use CTE to exclude job platforms
            query = text(
                """
                WITH job_platforms_to_exclude AS (
                    SELECT DISTINCT job_publisher as platform_name
                    FROM target.job_dashboard_base
                    WHERE is_job_platform = true
                    AND job_publisher IS NOT NULL
                    AND job_publisher != ''
                ),
                company_counts AS (
                    SELECT 
                        jdb.employer_name,
                        COUNT(*) as job_count
                    FROM target.job_dashboard_base jdb
                    LEFT JOIN job_platforms_to_exclude jpe 
                        ON LOWER(jdb.employer_name) LIKE LOWER('%' || jpe.platform_name || '%')
                    WHERE jdb.employer_name IS NOT NULL 
                        AND jdb.employer_name != ''
                        AND jpe.platform_name IS NULL
                    GROUP BY jdb.employer_name
                    ORDER BY job_count DESC
                    LIMIT 100
                )
                SELECT employer_name
                FROM company_counts
                ORDER BY employer_name
            """
            )
        else:
            # Simple query without platform exclusion
            query = text(
                """
                WITH company_counts AS (
                    SELECT 
                        employer_name,
                        COUNT(*) as job_count
                    FROM target.job_dashboard_base
                    WHERE employer_name IS NOT NULL AND employer_name != ''
                    GROUP BY employer_name
                    ORDER BY job_count DESC
                    LIMIT 100
                )
                SELECT employer_name
                FROM company_counts
                ORDER BY employer_name
            """
            )

        result = db.execute(query)
        companies = [row[0] for row in result]
        return companies

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching companies: {str(e)}")


@router.get("/available-publishers", response_model=list[str])
async def public_get_available_publishers(db: Session = Depends(get_db)):
    """
    Public endpoint for getting available publishers (no authentication required).
    Returns top 50 publishers for filter population on landing page.
    """
    try:
        # Limit to top 50 publishers for public access
        query = text(
            """
            WITH publisher_counts AS (
                SELECT 
                    publisher,
                    COUNT(*) as count
                FROM target.job_dashboard_base,
                     LATERAL jsonb_array_elements(apply_options::jsonb) as option,
                     LATERAL (option ->> 'publisher') as publisher
                WHERE apply_options IS NOT NULL 
                    AND apply_options::text != 'null'
                    AND apply_options::text != '[]'
                    AND publisher IS NOT NULL
                    AND publisher != ''
                GROUP BY publisher
                ORDER BY count DESC
                LIMIT 50
            )
            SELECT publisher
            FROM publisher_counts
            ORDER BY publisher
        """
        )

        result = db.execute(query)
        publishers = [row[0] for row in result]
        return publishers

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching publishers: {str(e)}")
