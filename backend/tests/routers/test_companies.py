"""
Unit tests for company endpoints

Tests the get_top_companies endpoint with various scenarios:
- Valid requests with different parameters
- Database mocking
- Error handling
"""

from unittest.mock import MagicMock, Mock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.routers.companies import get_top_companies


class TestGetTopCompanies:
    """Test suite for get_top_companies endpoint

    IMPORTANT: Frontend Usage Pattern
    ---------------------------------
    The frontend (companies.js store) ALWAYS sends these parameters:
    - limit: 20 (configurable per endpoint)
    - search_position_query: 'Data Engineer' (or selected position)
    - job_posted_at_date_from: Date (defaults to 30 days ago)
    - job_posted_at_date_to: Date (defaults to today)

    Optional filters:
    - employer_name: Company name if filtered
    - job_is_remote: 'true'/'false' if filtered
    - seniority: Seniority level if filtered

    See: frontend/src/stores/companies.js (_buildParams function)
    """

    def test_get_top_companies_with_typical_frontend_call(
        self, mock_db_session, sample_company_data, mock_get_job_platforms
    ):
        """Test get_top_companies exactly as frontend calls it (real-world usage)"""
        # Arrange
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = sample_company_data
        mock_db_session.execute.return_value = mock_result

        # Act - Exact pattern from frontend companies.js:48
        # const params = this._buildParams(20)
        # this.topCompanies = await fetchTopCompanies(params)
        result = get_top_companies(
            limit=20,  # Always sent
            search_position_query="Data Engineer",  # Default position
            job_posted_at_date_from="2024-01-01",  # Calculated from period
            job_posted_at_date_to="2024-12-31",  # Calculated from period
            employer_name=None,  # Not filtered
            job_is_remote=None,  # Not filtered
            seniority=None,  # Not filtered
            db=mock_db_session,
        )

        # Assert
        assert result == sample_company_data
        assert len(result) == 5

        # Verify all parameters are passed to query
        params = mock_db_session.execute.call_args[0][1]
        assert params["limit"] == 20
        assert params["search_position_query"] == "Data Engineer"
        assert params["job_posted_at_date_from"] == "2024-01-01"
        assert params["job_posted_at_date_to"] == "2024-12-31"

    def test_get_top_companies_with_custom_limit(self, mock_db_session, mock_get_job_platforms):
        """Test get_top_companies with custom limit parameter"""
        # Arrange
        limited_data = [
            {"employer_name": "Tech Corp", "job_count": 150},
            {"employer_name": "Innovation Labs", "job_count": 120},
        ]
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = limited_data
        mock_db_session.execute.return_value = mock_result

        # Act
        result = get_top_companies(
            limit=2,
            job_posted_at_date_from="2024-01-01",
            job_posted_at_date_to="2024-12-31",
            employer_name=None,
            job_is_remote=None,
            seniority=None,
            search_position_query=None,
            db=mock_db_session,
        )

        # Assert
        assert len(result) == 2
        assert result[0]["employer_name"] == "Tech Corp"

    def test_get_top_companies_with_date_filters(
        self, mock_db_session, sample_company_data, mock_get_job_platforms
    ):
        """Test get_top_companies with date range filters"""
        # Arrange
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = sample_company_data
        mock_db_session.execute.return_value = mock_result

        # Act
        result = get_top_companies(
            limit=20,
            job_posted_at_date_from="2024-01-01",
            job_posted_at_date_to="2024-12-31",
            employer_name=None,
            job_is_remote=None,
            seniority=None,
            search_position_query=None,
            db=mock_db_session,
        )

        # Assert
        assert result == sample_company_data
        # Verify that execute was called with parameters
        call_args = mock_db_session.execute.call_args
        assert call_args is not None
        # Check that date parameters are in the params dict
        params = call_args[0][1]
        assert "job_posted_at_date_from" in params
        assert "job_posted_at_date_to" in params
        assert params["job_posted_at_date_from"] == "2024-01-01"
        assert params["job_posted_at_date_to"] == "2024-12-31"

    def test_get_top_companies_with_employer_name_filter(
        self, mock_db_session, mock_get_job_platforms
    ):
        """Test get_top_companies filtered by specific employer name"""
        # Arrange
        filtered_data = [{"employer_name": "Tech Corp", "job_count": 150}]
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = filtered_data
        mock_db_session.execute.return_value = mock_result

        # Act
        result = get_top_companies(
            limit=20,
            employer_name="Tech Corp",
            job_posted_at_date_from=None,
            job_posted_at_date_to=None,
            job_is_remote=None,
            seniority=None,
            search_position_query=None,
            db=mock_db_session,
        )

        # Assert
        assert len(result) == 1
        assert result[0]["employer_name"] == "Tech Corp"
        # Verify employer_name parameter is passed
        params = mock_db_session.execute.call_args[0][1]
        assert params["employer_name"] == "Tech Corp"

    def test_get_top_companies_with_remote_filter(
        self, mock_db_session, sample_company_data, mock_get_job_platforms
    ):
        """Test get_top_companies filtered by remote jobs"""
        # Arrange
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = sample_company_data
        mock_db_session.execute.return_value = mock_result

        # Act
        result = get_top_companies(
            limit=20,
            job_posted_at_date_from="2024-01-01",
            job_posted_at_date_to="2024-12-31",
            employer_name=None,
            job_is_remote="true",
            seniority=None,
            search_position_query=None,
            db=mock_db_session,
        )

        # Assert
        assert result == sample_company_data
        # Verify the query includes remote filter
        query_text = str(mock_db_session.execute.call_args[0][0])
        assert "job_is_remote = true" in query_text

    def test_get_top_companies_with_seniority_filter(
        self, mock_db_session, sample_company_data, mock_get_job_platforms
    ):
        """Test get_top_companies filtered by seniority level"""
        # Arrange
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = sample_company_data
        mock_db_session.execute.return_value = mock_result

        # Act
        result = get_top_companies(
            limit=20,
            job_posted_at_date_from="2024-01-01",
            job_posted_at_date_to="2024-12-31",
            employer_name=None,
            job_is_remote=None,
            seniority="Senior",
            search_position_query=None,
            db=mock_db_session,
        )

        # Assert
        assert result == sample_company_data
        params = mock_db_session.execute.call_args[0][1]
        assert params["seniority"] == "Senior"

    def test_get_top_companies_with_position_query_filter(
        self, mock_db_session, sample_company_data, mock_get_job_platforms
    ):
        """Test get_top_companies filtered by position query"""
        # Arrange
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = sample_company_data
        mock_db_session.execute.return_value = mock_result

        # Act
        result = get_top_companies(
            limit=20,
            search_position_query="Software Engineer",
            job_posted_at_date_from=None,
            job_posted_at_date_to=None,
            employer_name=None,
            job_is_remote=None,
            seniority=None,
            db=mock_db_session,
        )

        # Assert
        assert result == sample_company_data
        params = mock_db_session.execute.call_args[0][1]
        assert params["search_position_query"] == "Software Engineer"

    def test_get_top_companies_with_all_filters(
        self, mock_db_session, sample_company_data, mock_get_job_platforms
    ):
        """Test get_top_companies with all filters combined"""
        # Arrange
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = sample_company_data
        mock_db_session.execute.return_value = mock_result

        # Act
        result = get_top_companies(
            limit=10,
            job_posted_at_date_from="2024-01-01",
            job_posted_at_date_to="2024-12-31",
            employer_name="Tech Corp",
            job_is_remote="true",
            seniority="Senior",
            search_position_query="Python Developer",
            db=mock_db_session,
        )

        # Assert
        assert result == sample_company_data
        params = mock_db_session.execute.call_args[0][1]
        assert params["limit"] == 10
        assert params["job_posted_at_date_from"] == "2024-01-01"
        assert params["job_posted_at_date_to"] == "2024-12-31"
        assert params["employer_name"] == "Tech Corp"
        assert params["seniority"] == "Senior"
        assert params["search_position_query"] == "Python Developer"

    def test_get_top_companies_empty_results(self, mock_db_session, mock_get_job_platforms):
        """Test get_top_companies when no companies match filters"""
        # Arrange
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = []
        mock_db_session.execute.return_value = mock_result

        # Act
        result = get_top_companies(
            limit=20,
            job_posted_at_date_from="2024-01-01",
            job_posted_at_date_to="2024-12-31",
            employer_name=None,
            job_is_remote=None,
            seniority=None,
            search_position_query=None,
            db=mock_db_session,
        )

        # Assert
        assert result == []
        assert len(result) == 0

    def test_get_top_companies_with_job_platforms(
        self, mock_db_session, sample_company_data, mock_get_job_platforms
    ):
        """Test that job platforms are excluded from results"""
        # Arrange
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = sample_company_data
        mock_db_session.execute.return_value = mock_result

        # Act
        result = get_top_companies(
            limit=20,
            job_posted_at_date_from="2024-01-01",
            job_posted_at_date_to="2024-12-31",
            employer_name=None,
            job_is_remote=None,
            seniority=None,
            search_position_query=None,
            db=mock_db_session,
        )

        # Assert
        assert result == sample_company_data
        # Verify that the query includes platform exclusion logic
        query_text = str(mock_db_session.execute.call_args[0][0])
        assert "job_platforms_to_exclude" in query_text

    def test_get_top_companies_without_job_platforms(
        self, mock_db_session, sample_company_data, mock_get_job_platforms_empty
    ):
        """Test query structure when no job platforms exist"""
        # Arrange
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = sample_company_data
        mock_db_session.execute.return_value = mock_result

        # Act
        result = get_top_companies(
            limit=20,
            job_posted_at_date_from="2024-01-01",
            job_posted_at_date_to="2024-12-31",
            employer_name=None,
            job_is_remote=None,
            seniority=None,
            search_position_query=None,
            db=mock_db_session,
        )

        # Assert
        assert result == sample_company_data
        # Verify simpler query is used when no platforms to exclude
        query_text = str(mock_db_session.execute.call_args[0][0])
        assert "job_platforms_to_exclude" not in query_text

    # Error Handling Tests

    def test_get_top_companies_database_error(self, mock_db_session, mock_get_job_platforms):
        """Test that database errors are handled gracefully"""
        # Arrange
        mock_db_session.execute.side_effect = SQLAlchemyError("Database connection error")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_top_companies(
                limit=20,
                job_posted_at_date_from=None,
                job_posted_at_date_to=None,
                employer_name=None,
                job_is_remote=None,
                seniority=None,
                search_position_query=None,
                db=mock_db_session,
            )

        assert exc_info.value.status_code == 500
        assert "Internal server error" in str(exc_info.value.detail)

    def test_get_top_companies_unexpected_error(self, mock_db_session, mock_get_job_platforms):
        """Test that unexpected errors return 500 status"""
        # Arrange
        mock_db_session.execute.side_effect = Exception("Unexpected error")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_top_companies(
                limit=20,
                job_posted_at_date_from=None,
                job_posted_at_date_to=None,
                employer_name=None,
                job_is_remote=None,
                seniority=None,
                search_position_query=None,
                db=mock_db_session,
            )

        assert exc_info.value.status_code == 500
        assert "Internal server error" in str(exc_info.value.detail)
