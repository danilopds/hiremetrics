"""Core dashboard data endpoints"""
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..schemas import JobDashboardBase, TopSkill
from ..utils.cache import cache_result
from ..utils.query_builder import SecureQueryBuilder

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/jobs", response_model=list[JobDashboardBase])
def get_job_dashboard_base(
    limit: int = Query(1000, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    job_posted_at_date: Optional[str] = Query(
        None, description="Filter by job posted date (YYYY-MM-DD)"
    ),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    job_city: Optional[str] = Query(None, description="Filter by job city"),
    job_state: Optional[str] = Query(None, description="Filter by job state"),
    job_is_remote: Optional[str] = Query(
        None, description="Filter by remote (true/false)"
    ),
    employer_name: Optional[str] = Query(None, description="Filter by company name"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get job dashboard data with comprehensive filtering"""
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 10000
        )
        validated_offset = SecureQueryBuilder.validate_integer_input(
            offset, "offset", 0
        )

        # Build secure filters
        filters = {}
        params = {"limit": validated_limit, "offset": validated_offset}

        # Validate date inputs
        if job_posted_at_date not in (None, "", "null"):
            validated_date = SecureQueryBuilder.validate_date_input(
                job_posted_at_date, "job_posted_at_date"
            )
            filters["job_posted_at_date >= :job_posted_at_date"] = validated_date
            params["job_posted_at_date"] = validated_date

        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters["job_posted_at_date >= :job_posted_at_date_from"] = (
                validated_date_from
            )
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters["job_posted_at_date <= :job_posted_at_date_to"] = validated_date_to
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if job_city not in (None, "", "null"):
            validated_city = SecureQueryBuilder.validate_text_input(
                job_city, "job_city"
            )
            filters["job_city ILIKE :job_city"] = validated_city
            params["job_city"] = f"%{validated_city}%"

        if job_state not in (None, "", "null"):
            validated_state = SecureQueryBuilder.validate_text_input(
                job_state, "job_state"
            )
            filters["job_state ILIKE :job_state"] = validated_state
            params["job_state"] = f"%{validated_state}%"

        # Validate boolean input
        if job_is_remote not in (None, "", "null"):
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            filters["job_is_remote = :job_is_remote"] = validated_remote
            params["job_is_remote"] = validated_remote

        if employer_name not in (None, "", "null"):
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters["employer_name = :employer_name"] = validated_employer
            params["employer_name"] = validated_employer

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters["search_position_query = :search_position_query"] = (
                validated_position
            )
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters.keys())}" if filters else ""

        # Use parameterized query
        base_query = """
            SELECT job_id, job_title, job_employment_type, job_is_remote, job_posted_at_date, 
                   job_publisher, employer_name, job_city, job_state, apply_options, 
                   created_at, updated_at, created_by, updated_by
            FROM target.job_dashboard_base
        """

        full_query = f"{base_query} {where_clause} ORDER BY job_posted_at_date DESC LIMIT :limit OFFSET :offset"
        query = text(full_query)

        result = db.execute(query, params)
        jobs = result.mappings().all()
        return jobs

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/top-skills", response_model=list[TopSkill])
@cache_result(ttl=300, key_prefix="top_skills")  # Cache for 5 minutes
def get_top_skills(
    limit: int = Query(10, ge=1, le=1000),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get top skills with optional filters"""
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 1000
        )

        # Build secure filters
        filters = {}
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters["job_posted_at_date >= :job_posted_at_date_from"] = (
                validated_date_from
            )
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters["job_posted_at_date <= :job_posted_at_date_to"] = validated_date_to
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters["seniority = :seniority"] = validated_seniority
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters["search_position_query = :search_position_query"] = (
                validated_position
            )
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters.keys())}" if filters else ""

        # Optimized query - avoid complex CTE and JOIN operations
        if seniority is None:
            # When no seniority filter, first get top skills by total count, then get all seniority levels for those skills
            # This ensures we get complete seniority breakdown for the top skills
            base_query = """
                WITH top_skills AS (
                    SELECT 
                        skill,
                        SUM(skill_count) as total_count
                    FROM target.job_skills
                    {where_clause}
                    GROUP BY skill
                    ORDER BY total_count DESC
                    LIMIT :limit
                )
                SELECT 
                    js.skill,
                    js.seniority,
                    SUM(js.skill_count) as skill_count,
                    MAX(ts.total_count) as total_count
                FROM target.job_skills js
                INNER JOIN top_skills ts ON js.skill = ts.skill
                {where_clause}
                GROUP BY js.skill, js.seniority
                ORDER BY total_count DESC, js.skill, skill_count DESC
            """
            full_query = base_query.format(where_clause=where_clause)
        else:
            # If seniority is specified, include seniority field for API consistency
            base_query = """
                SELECT skill, seniority, SUM(skill_count) as skill_count
                FROM target.job_skills
                {where_clause}
                GROUP BY skill, seniority
                ORDER BY skill_count DESC
                LIMIT :limit
            """
            full_query = base_query.format(where_clause=where_clause)

        query = text(full_query)
        result = db.execute(query, params)
        skills = result.mappings().all()

        return skills

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Error in top-skills endpoint: {e}")
        if "timeout" in str(e).lower() or "connection" in str(e).lower():
            raise HTTPException(
                status_code=503,
                detail="Database temporarily unavailable. Please try again.",
            )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/skills-trend")
def get_skills_trend(
    request: Request,
    limit: int = Query(
        50, ge=1, le=100
    ),  # Increased from 5,20 to 50,100 to allow more skills for chart
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get skills trend data over time"""
    try:
        # Validate and sanitize inputs
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 100
        )

        # Build secure filters
        filters = {}
        params = {"limit": validated_limit}

        # Validate date inputs
        if job_posted_at_date_from not in (None, "", "null"):
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters["job_posted_at_date >= :job_posted_at_date_from"] = (
                validated_date_from
            )
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to not in (None, "", "null"):
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters["job_posted_at_date <= :job_posted_at_date_to"] = validated_date_to
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if seniority not in (None, "", "null"):
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters["seniority = :seniority"] = validated_seniority
            params["seniority"] = validated_seniority

        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters["search_position_query = :search_position_query"] = (
                validated_position
            )
            params["search_position_query"] = validated_position

        # Extract and validate skills from query parameters
        skills = []
        query_params = dict(request.query_params)

        # Handle both skills[] and skills parameters
        if "skills[]" in query_params:
            skills_param = query_params["skills[]"]
            if isinstance(skills_param, str):
                skills = [skills_param]
            else:
                skills = skills_param
        elif "skills" in query_params:
            skills_param = query_params["skills"]
            if isinstance(skills_param, str):
                skills = [skills_param]
            else:
                skills = skills_param

        # Also check for multiple skills[] parameters
        for key, value in request.query_params.multi_items():
            if key == "skills[]":
                if value not in skills:
                    skills.append(value)
            elif key == "skills":
                if value not in skills:
                    skills.append(value)

        # Handle skills filtering with validation
        if skills and len(skills) > 0:
            # Filter out empty strings and None values, then validate
            valid_skills = []
            for skill in skills:
                if skill and skill.strip():
                    validated_skill = SecureQueryBuilder.validate_text_input(
                        skill, "skill"
                    )
                    valid_skills.append(validated_skill)

            if valid_skills:
                # Create dynamic placeholders for IN clause
                skill_placeholders = ", ".join(
                    [f":skill_{i}" for i in range(len(valid_skills))]
                )
                filters[f"skill IN ({skill_placeholders})"] = valid_skills
                for i, skill in enumerate(valid_skills):
                    params[f"skill_{i}"] = skill
        else:
            # Get top N skills if not provided
            where_clause_for_top = (
                f"WHERE {' AND '.join(filters.keys())}" if filters else ""
            )
            top_skills_query = text(
                f"""
                SELECT skill
                FROM target.job_skills
                {where_clause_for_top}
                GROUP BY skill
                ORDER BY SUM(skill_count) DESC
                LIMIT :limit
            """
            )
            params_for_top = {**params, "limit": validated_limit}
            result = db.execute(top_skills_query, params_for_top)
            top_skills = [row[0] for row in result]

            if top_skills:
                # Create dynamic placeholders for IN clause
                skill_placeholders = ", ".join(
                    [f":skill_{i}" for i in range(len(top_skills))]
                )
                filters[f"skill IN ({skill_placeholders})"] = top_skills
                for i, skill in enumerate(top_skills):
                    params[f"skill_{i}"] = skill

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters.keys())}" if filters else ""

        # Use parameterized query
        base_query = """
            SELECT 
                job_posted_at_date,
                skill,
                seniority,
                SUM(skill_count) as skill_count
            FROM target.job_skills
            {where_clause}
            GROUP BY job_posted_at_date, skill, seniority
            ORDER BY job_posted_at_date, skill, seniority
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        trends = result.mappings().all()
        return trends

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Error in skills-trend endpoint: {e}")
        if "timeout" in str(e).lower() or "connection" in str(e).lower():
            raise HTTPException(
                status_code=503,
                detail="Database temporarily unavailable. Please try again.",
            )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/available-skills", response_model=list[str])
@cache_result(ttl=600, key_prefix="available_skills")  # Cache for 10 minutes
def get_available_skills(
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get list of all available skills from the database."""
    try:
        # Build secure filters
        filters = {}
        params = {}

        # Validate text input
        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters["search_position_query = :search_position_query"] = (
                validated_position
            )
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters.keys())}" if filters else ""

        # Use parameterized query
        base_query = """
            SELECT DISTINCT skill
            FROM target.job_skills
            {where_clause}
            ORDER BY skill
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        skills = [row[0] for row in result]
        return skills

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/available-seniority-levels", response_model=list[str])
@cache_result(ttl=600, key_prefix="available_seniority")  # Cache for 10 minutes
def get_available_seniority_levels(
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get list of all available seniority levels from the database."""
    try:
        # Build secure filters
        filters = ["seniority IS NOT NULL AND seniority != ''"]
        params = {}

        # Validate text input
        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}"

        # Use parameterized query
        base_query = """
            SELECT DISTINCT seniority
            FROM target.job_skills
            {where_clause}
            ORDER BY seniority DESC
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        seniority_levels = [row[0] for row in result]
        return seniority_levels

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/available-positions", response_model=list[str])
@cache_result(ttl=1800, key_prefix="available_positions")  # Cache for 30 minutes
def get_available_positions(db: Session = Depends(get_db)):
    """Get list of all available positions from the database."""
    try:
        # Use parameterized query (no user input, so safe)
        query = text(
            """
            SELECT DISTINCT search_position_query
            FROM target.job_dashboard_base
            WHERE search_position_query IS NOT NULL AND search_position_query != ''
            ORDER BY search_position_query
        """
        )

        result = db.execute(query)
        positions = [row[0] for row in result]
        return positions

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/locations", response_model=list[dict])
def get_filtered_locations(
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    job_posted_at_date_from: Optional[str] = Query(
        None, description="Filter by job posted date from (YYYY-MM-DD)"
    ),
    job_posted_at_date_to: Optional[str] = Query(
        None, description="Filter by job posted date to (YYYY-MM-DD)"
    ),
    db: Session = Depends(get_db),
):
    """Get filtered city/state locations based on position and date filters."""
    try:
        # Build secure filters
        filters = []
        params = {}

        # Validate text input
        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

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

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Use parameterized query
        base_query = """
            SELECT DISTINCT job_city, job_state
            FROM target.job_dashboard_base
            {where_clause}
            AND job_city IS NOT NULL AND job_city != ''
            AND job_state IS NOT NULL AND job_state != ''
            ORDER BY job_city, job_state
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        locations = [
            {"title": row[0], "state": row[1]} for row in result if row[0] and row[1]
        ]
        return locations

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/available-publishers", response_model=list[str])
@cache_result(ttl=600, key_prefix="available_publishers")  # Cache for 10 minutes
def get_available_publishers(
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get list of all available publishers from the database."""
    try:
        # Build secure filters
        filters = []
        params = {}

        # Validate text input
        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        # Use parameterized query
        base_query = """
            WITH expanded_options AS (
                SELECT DISTINCT (jsonb_array_elements(apply_options::jsonb) ->> 'publisher') as publisher
                FROM target.job_dashboard_base
                {where_clause}
            )
            SELECT publisher
            FROM expanded_options
            WHERE publisher IS NOT NULL AND publisher != ''
            ORDER BY publisher
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        publishers = [row[0] for row in result]
        return publishers

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/available-companies", response_model=list[str])
@cache_result(ttl=600, key_prefix="available_companies")  # Cache for 10 minutes
def get_available_companies(
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    db: Session = Depends(get_db),
):
    """Get list of all available companies from the database."""
    try:
        from ..services.query_service import get_job_platforms

        # Build secure filters
        filters = []
        params = {}

        # Validate text input
        if search_position_query not in (None, "", "null"):
            validated_position = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Build secure WHERE clause
        if filters:
            where_clause = f"WHERE {' AND '.join(filters)} AND employer_name IS NOT NULL AND employer_name != ''"
        else:
            where_clause = "WHERE employer_name IS NOT NULL AND employer_name != ''"

        # Get job platforms to exclude from company data
        job_platforms = get_job_platforms(db)

        # Add job platform exclusion logic
        if job_platforms:
            # Create regex pattern for case-insensitive matching
            platform_patterns = []
            for platform in job_platforms:
                # Escape special regex characters and create case-insensitive pattern
                escaped_platform = (
                    platform.replace("\\", "\\\\")
                    .replace(".", "\\.")
                    .replace("*", "\\*")
                    .replace("+", "\\+")
                    .replace("?", "\\?")
                    .replace("^", "\\^")
                    .replace("$", "\\$")
                    .replace("[", "\\[")
                    .replace("]", "\\]")
                    .replace("(", "\\(")
                    .replace(")", "\\)")
                    .replace("|", "\\|")
                )
                platform_patterns.append(
                    f"LOWER(employer_name) NOT LIKE LOWER('%{escaped_platform}%')"
                )

            # Add the exclusion condition to the WHERE clause
            if where_clause:
                where_clause = where_clause.replace(
                    "WHERE", f"WHERE {' AND '.join(platform_patterns)} AND"
                )
            else:
                where_clause = f"WHERE {' AND '.join(platform_patterns)}"

        # Use parameterized query
        base_query = """
            SELECT DISTINCT employer_name
            FROM target.job_dashboard_base
            {where_clause}
            ORDER BY employer_name
        """

        full_query = base_query.format(where_clause=where_clause)
        query = text(full_query)

        result = db.execute(query, params)
        companies = [row[0] for row in result]
        return companies

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        print(f"Error in get_available_companies: {str(e)}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/job-locations-geo")
def get_job_locations_geo(
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
    job_city: Optional[str] = Query(None, description="Filter by city"),
    job_state: Optional[str] = Query(None, description="Filter by state"),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    limit: int = Query(500, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Get geographic job location data with comprehensive filtering"""
    try:
        # Validate limit parameter
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 1000
        )

        filters = []
        params = {"limit": validated_limit}

        # Validate and add date filters
        if job_posted_at_date_from:
            validated_date_from = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_from, "job_posted_at_date_from"
            )
            filters.append("job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if job_posted_at_date_to:
            validated_date_to = SecureQueryBuilder.validate_date_input(
                job_posted_at_date_to, "job_posted_at_date_to"
            )
            filters.append("job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate and add text filters
        if employer_name:
            validated_employer = SecureQueryBuilder.validate_text_input(
                employer_name, "employer_name"
            )
            filters.append("employer_name = :employer_name")
            params["employer_name"] = validated_employer

        if seniority:
            validated_seniority = SecureQueryBuilder.validate_text_input(
                seniority, "seniority"
            )
            filters.append("seniority = :seniority")
            params["seniority"] = validated_seniority

        if job_city:
            validated_city = SecureQueryBuilder.validate_text_input(
                job_city, "job_city"
            )
            filters.append("job_city = :job_city")
            params["job_city"] = validated_city

        if job_state:
            validated_state = SecureQueryBuilder.validate_text_input(
                job_state, "job_state"
            )
            filters.append("job_state = :job_state")
            params["job_state"] = validated_state

        # Validate and add search position query with secure ILIKE
        if search_position_query:
            validated_search = SecureQueryBuilder.validate_text_input(
                search_position_query, "search_position_query"
            )
            filters.append("search_position_query ILIKE :search_position_query")
            params["search_position_query"] = f"%{validated_search}%"

        # Validate and add boolean filter
        if job_is_remote is not None:
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                job_is_remote, "job_is_remote"
            )
            filters.append("job_is_remote = :job_is_remote")
            params["job_is_remote"] = validated_remote

        # Always filter out null or placeholder values (static filters)
        location_filters = [
            "job_city IS NOT NULL",
            "job_city != 'Brasil (N/A)'",
            "job_city != ''",
            "job_state IS NOT NULL",
            "job_state != 'Brasil (N/A)'",
            "job_state != ''",
        ]

        # Combine all filters
        all_filters = filters + location_filters
        where_clause = f"WHERE {' AND '.join(all_filters)}" if all_filters else ""

        query = text(
            f"""
            SELECT 
                job_city,
                job_state,
                COUNT(*) as job_count
            FROM target.job_dashboard_base
            {where_clause}
            GROUP BY job_city, job_state
            ORDER BY job_count DESC
            LIMIT :limit
        """
        )

        result = db.execute(query, params)
        locations = result.mappings().all()

        return locations

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/employment-type-distribution")
def get_employment_type_distribution(
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
    """Get employment type distribution."""
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
                    job_employment_type,
                    COUNT(job_id) as job_count,
                    ROUND(COUNT(job_id) * 100.0 / SUM(COUNT(job_id)) OVER (), 2) as percentage
                FROM target.job_dashboard_base
                WHERE employer_name = :employer_name
                {additional_where}
                GROUP BY job_employment_type
                ORDER BY job_count DESC
            """
            full_query = base_query.format(additional_where=additional_where)
        else:
            base_query = """
                SELECT 
                    job_employment_type,
                    COUNT(job_id) as job_count,
                    ROUND(COUNT(job_id) * 100.0 / SUM(COUNT(job_id)) OVER (), 2) as percentage
                FROM target.job_dashboard_base
                {where_clause}
                GROUP BY job_employment_type
                ORDER BY job_count DESC
            """
            full_query = base_query.format(where_clause=where_clause)

        query = text(full_query)
        result = db.execute(query, params)
        distribution = result.mappings().all()
        return distribution

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

