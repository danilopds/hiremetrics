"""Skills filtering endpoints"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..schemas import CSVExportFilters
from ..services.query_service import build_where_clause_and_params
from ..utils.auth_utils import get_current_user
from ..utils.query_builder import SecureQueryBuilder

router = APIRouter()


@router.get("/jobs", response_model=list[schemas.JobExportData])
async def get_jobs_by_skills(
    skills: str = Query(..., description="Comma-separated list of skills to filter by"),
    job_posted_at_date_from: Optional[str] = Query(None),
    job_posted_at_date_to: Optional[str] = Query(None),
    search_position_query: Optional[str] = Query(
        None, description="Filter by position query"
    ),
    employer_names: Optional[str] = Query(
        None, description="Comma-separated list of employer names"
    ),
    publishers: Optional[str] = Query(
        None, description="Comma-separated list of publishers"
    ),
    seniority_levels: Optional[str] = Query(
        None, description="Comma-separated list of seniority levels"
    ),
    employment_types: Optional[str] = Query(
        None, description="Comma-separated list of employment types"
    ),
    cities: Optional[str] = Query(None, description="Comma-separated list of cities"),
    states: Optional[str] = Query(None, description="Comma-separated list of states"),
    job_is_remote: Optional[bool] = Query(None),
    is_direct: Optional[bool] = Query(None),
    limit: int = Query(10000, ge=1, le=50000),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get jobs filtered by specific skills with optimized query for skills filtering.
    This endpoint uses a specialized query that efficiently searches for skills in the extracted_skills field.
    """
    try:
        # Validate limit parameter
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 50000
        )

        # Parse and validate comma-separated parameters
        filters = CSVExportFilters(
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

        # Build secure WHERE clause with validated filters
        where_clause, params = build_where_clause_and_params(filters)
        params["limit"] = validated_limit

        # Simplified skills filtering query
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

