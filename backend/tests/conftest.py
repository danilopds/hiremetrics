"""Pytest configuration and fixtures for testing"""

import os
import sys
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, Mock

import pytest
from sqlalchemy.orm import Session

# Set up test environment variables before any app imports
env_test_file = Path(__file__).parent.parent / ".env.test"
if env_test_file.exists():
    from dotenv import load_dotenv

    load_dotenv(env_test_file)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Ensure test environment is properly configured"""
    # Verify required environment variables are set
    required_vars = ["DATABASE_URL", "JWT_SECRET_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables for testing: {', '.join(missing_vars)}. "
            "Please ensure .env.test exists or environment variables are set."
        )

    yield

    # Cleanup after all tests (if needed)
    pass


@pytest.fixture
def mock_db_session() -> Mock:
    """Create a mock database session for testing"""
    db = MagicMock(spec=Session)
    return db


@pytest.fixture
def mock_db_result():
    """Create a mock database result object"""
    mock_result = MagicMock()
    return mock_result


@pytest.fixture
def sample_company_data():
    """Sample company data for testing"""
    return [
        {"employer_name": "Tech Corp", "job_count": 150},
        {"employer_name": "Innovation Labs", "job_count": 120},
        {"employer_name": "StartUp Inc", "job_count": 95},
        {"employer_name": "Digital Solutions", "job_count": 80},
        {"employer_name": "Cloud Systems", "job_count": 65},
    ]


@pytest.fixture
def sample_job_platforms():
    """Sample job platform names for testing"""
    return ["LinkedIn", "Indeed", "Glassdoor", "ZipRecruiter"]


@pytest.fixture
def mock_get_job_platforms(monkeypatch, sample_job_platforms):
    """Mock the get_job_platforms function

    IMPORTANT: We patch where it's USED (in companies module),
    not where it's DEFINED (in query_service module).
    """

    def mock_func(db):
        return sample_job_platforms

    # Patch in the companies module where it's imported and used
    from app.routers import companies

    monkeypatch.setattr(companies, "get_job_platforms", mock_func)
    return mock_func


@pytest.fixture
def mock_get_job_platforms_empty(monkeypatch):
    """Mock the get_job_platforms function to return empty list

    IMPORTANT: We patch where it's USED (in companies module),
    not where it's DEFINED (in query_service module).
    """

    def mock_func(db):
        return []

    # Patch in the companies module where it's imported and used
    from app.routers import companies

    monkeypatch.setattr(companies, "get_job_platforms", mock_func)
    return mock_func
