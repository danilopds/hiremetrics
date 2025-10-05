"""CSV export and reporting endpoints

This module contains all reporting and export endpoints including:
- CSV export with filtering
- Export record counting
- Export preview
- Available filter options (locations, employment types, etc.)
"""

import csv
import io
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..schemas import CSVExportRequest, ExportCountResponse
from ..services.query_service import (build_where_clause_and_params,
                                      get_job_platforms)
from ..utils.auth_utils import get_current_user
from ..utils.query_builder import SecureQueryBuilder

router = APIRouter()


@router.post("/count-export-records", response_model=ExportCountResponse)
async def count_export_records(
    request: CSVExportRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Count the number of records that would be exported with the given filters"""
    try:
        # Validate max_records parameter
        validated_max_records = SecureQueryBuilder.validate_integer_input(
            request.max_records, "max_records", 1, 50000
        )

        # Build secure WHERE clause with validated filters
        where_clause, params = build_where_clause_and_params(request.filters)

        count_query = text(
            f"""
            SELECT COUNT(*) as total_count
            FROM target.job_dashboard_base jdb
            {where_clause}
        """
        )

        result = db.execute(count_query, params)
        count = result.scalar()

        return ExportCountResponse(count=count, max_allowed=validated_max_records)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/export-csv")
async def export_csv(
    request: CSVExportRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Export job data as CSV with comprehensive filtering"""
    try:
        # Validate max records with secure input validation
        validated_max_records = SecureQueryBuilder.validate_integer_input(
            request.max_records, "max_records", 1, 50000
        )

        # Build secure WHERE clause with validated filters
        where_clause, params = build_where_clause_and_params(request.filters)
        params["limit"] = validated_max_records

        # Build the main query to get all job data
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

        # Create CSV in memory with proper UTF-8 encoding for Brazilian Portuguese
        output = io.StringIO()
        writer = csv.writer(output)

        # Write CSV headers
        headers = [
            "job_id",
            "job_title",
            "employer_name",
            "job_posted_at_date",
            "job_city",
            "job_state",
            "seniority",
            "job_employment_type",
            "job_is_remote",
            "job_publisher",
            "extracted_skills",
            "apply_options",
            "search_position_query",
            "created_at",
            "updated_at",
        ]
        writer.writerow(headers)

        # Write data rows with proper string handling
        for job in jobs:
            row = [
                str(job.job_id or ""),
                str(job.job_title or ""),
                str(job.employer_name or ""),
                str(job.job_posted_at_date) if job.job_posted_at_date else "",
                str(job.job_city or ""),
                str(job.job_state or ""),
                str(job.seniority or ""),
                str(job.job_employment_type or ""),
                "Sim" if job.job_is_remote else "Não",  # Portuguese Yes/No
                str(job.job_publisher or ""),
                str(job.extracted_skills or ""),
                str(job.apply_options or ""),
                str(job.search_position_query or ""),
                job.created_at.isoformat() if job.created_at else "",
                job.updated_at.isoformat() if job.updated_at else "",
            ]
            writer.writerow(row)

        # Prepare response with UTF-8 BOM for proper encoding recognition
        output.seek(0)
        csv_content = output.getvalue()
        output.close()

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jobs_export_{timestamp}.csv"

        # Return as streaming response with UTF-8 BOM
        def generate():
            # UTF-8 BOM (Byte Order Mark) for proper encoding detection
            yield b"\xef\xbb\xbf"
            yield csv_content.encode("utf-8")

        return StreamingResponse(
            generate(),
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{filename}",
                "Content-Type": "text/csv; charset=utf-8",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error exporting CSV: {str(e)}")


@router.get("/preview-export", response_model=list[schemas.JobExportData])
async def preview_export(
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
    skills: Optional[str] = Query(None, description="Comma-separated list of skills"),
    job_is_remote: Optional[bool] = Query(None),
    is_direct: Optional[bool] = Query(None),
    limit: int = Query(10, ge=1, le=1000),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Preview the first N records that would be exported"""
    try:
        # Validate limit parameter
        validated_limit = SecureQueryBuilder.validate_integer_input(
            limit, "limit", 1, 1000
        )

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


@router.get("/available-locations", response_model=dict)
async def get_available_locations(db: Session = Depends(get_db)):
    """Get available cities and states for filtering"""
    try:
        query = text(
            """
            SELECT DISTINCT 
                job_city,
                job_state
            FROM target.job_dashboard_base
            WHERE job_city IS NOT NULL AND job_state IS NOT NULL
            ORDER BY job_state, job_city
        """
        )

        result = db.execute(query)
        locations = result.mappings().all()

        cities = sorted(list(set([loc.job_city for loc in locations if loc.job_city])))
        states = sorted(
            list(set([loc.job_state for loc in locations if loc.job_state]))
        )

        return {"cities": cities, "states": states}

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error fetching locations: {str(e)}"
        )


@router.get("/available-employment-types", response_model=list[str])
async def get_available_employment_types(db: Session = Depends(get_db)):
    """Get available employment types for filtering"""
    try:
        query = text(
            """
            SELECT DISTINCT job_employment_type
            FROM target.job_dashboard_base
            WHERE job_employment_type IS NOT NULL
            ORDER BY job_employment_type
        """
        )

        result = db.execute(query)
        types = [row[0] for row in result.fetchall()]
        return types

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error fetching employment types: {str(e)}"
        )
