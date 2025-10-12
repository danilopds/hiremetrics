"""Common query builders and database helpers"""

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..schemas import CSVExportFilters
from ..utils.query_builder import SecureQueryBuilder


def get_job_platforms(db: Session) -> list[str]:
    """Get list of job platform names that should be excluded from company data"""
    try:
        query = text(
            """
            SELECT DISTINCT job_publisher
            FROM target.job_dashboard_base
            WHERE is_job_platform = true
            AND job_publisher IS NOT NULL
            AND job_publisher != ''
        """
        )

        result = db.execute(query)
        platforms = [row[0] for row in result]
        return platforms
    except Exception as e:
        print(f"ERROR getting job platforms: {str(e)}")
        return []


def build_where_clause_and_params(filters: CSVExportFilters):
    """Build WHERE clause and parameters from filters with comprehensive input validation"""
    try:
        conditions = []
        params = {}

        # Validate date inputs
        if filters.job_posted_at_date_from:
            validated_date_from = SecureQueryBuilder.validate_date_input(
                filters.job_posted_at_date_from, "job_posted_at_date_from"
            )
            conditions.append("jdb.job_posted_at_date >= :job_posted_at_date_from")
            params["job_posted_at_date_from"] = validated_date_from

        if filters.job_posted_at_date_to:
            validated_date_to = SecureQueryBuilder.validate_date_input(
                filters.job_posted_at_date_to, "job_posted_at_date_to"
            )
            conditions.append("jdb.job_posted_at_date <= :job_posted_at_date_to")
            params["job_posted_at_date_to"] = validated_date_to

        # Validate text inputs
        if filters.search_position_query:
            validated_position = SecureQueryBuilder.validate_text_input(
                filters.search_position_query, "search_position_query"
            )
            conditions.append("jdb.search_position_query = :search_position_query")
            params["search_position_query"] = validated_position

        # Validate array inputs with individual element validation
        if filters.employer_names:
            validated_employers = []
            for employer in filters.employer_names:
                validated_employer = SecureQueryBuilder.validate_text_input(
                    employer, "employer_name"
                )
                validated_employers.append(validated_employer)
            conditions.append("jdb.employer_name = ANY(:employer_names)")
            params["employer_names"] = validated_employers

        if filters.seniority_levels:
            validated_seniorities = []
            for seniority in filters.seniority_levels:
                validated_seniority = SecureQueryBuilder.validate_text_input(seniority, "seniority")
                validated_seniorities.append(validated_seniority)
            conditions.append("jdb.seniority = ANY(:seniority_levels)")
            params["seniority_levels"] = validated_seniorities

        if filters.employment_types:
            validated_employment_types = []
            for emp_type in filters.employment_types:
                validated_emp_type = SecureQueryBuilder.validate_text_input(
                    emp_type, "employment_type"
                )
                validated_employment_types.append(validated_emp_type)
            conditions.append("jdb.job_employment_type = ANY(:employment_types)")
            params["employment_types"] = validated_employment_types

        if filters.cities:
            validated_cities = []
            for city in filters.cities:
                validated_city = SecureQueryBuilder.validate_text_input(city, "city")
                validated_cities.append(validated_city)
            conditions.append("jdb.job_city = ANY(:cities)")
            params["cities"] = validated_cities

        if filters.states:
            validated_states = []
            for state in filters.states:
                validated_state = SecureQueryBuilder.validate_text_input(state, "state")
                validated_states.append(validated_state)
            conditions.append("jdb.job_state = ANY(:states)")
            params["states"] = validated_states

        # Validate boolean inputs
        if filters.job_is_remote is not None:
            validated_remote = SecureQueryBuilder.validate_boolean_input(
                filters.job_is_remote, "job_is_remote"
            )
            conditions.append("jdb.job_is_remote = :job_is_remote")
            params["job_is_remote"] = validated_remote

        if filters.is_direct is not None:
            validated_direct = SecureQueryBuilder.validate_boolean_input(
                filters.is_direct, "is_direct"
            )
            conditions.append(
                """
                EXISTS (
                    SELECT 1 FROM jsonb_array_elements(jdb.apply_options::jsonb) AS ao
                    WHERE (ao ->> 'is_direct')::boolean = :is_direct
                )
            """
            )
            params["is_direct"] = validated_direct

        # Handle publishers and skills separately as they involve array operations
        if filters.publishers:
            validated_publishers = []
            for publisher in filters.publishers:
                validated_publisher = SecureQueryBuilder.validate_text_input(publisher, "publisher")
                validated_publishers.append(validated_publisher)
            conditions.append(
                """
                EXISTS (
                    SELECT 1 FROM jsonb_array_elements(jdb.apply_options::jsonb) AS ao
                    WHERE ao ->> 'publisher' = ANY(:publishers)
                )
            """
            )
            params["publishers"] = validated_publishers

        if filters.skills:
            validated_skills = []
            for skill in filters.skills:
                validated_skill = SecureQueryBuilder.validate_text_input(skill, "skill")
                validated_skills.append(validated_skill)
            conditions.append(
                """
                EXISTS (
                    SELECT 1 FROM jsonb_array_elements_text(jdb.extracted_skills::jsonb) AS skill
                    WHERE skill = ANY(:skills)
                )
            """
            )
            params["skills"] = validated_skills

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        return where_clause, params

    except ValueError as e:
        raise ValueError(f"Invalid filter input: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error building filter conditions: {str(e)}")
