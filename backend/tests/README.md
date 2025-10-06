# Backend Tests

This directory contains all unit and integration tests for the backend application.

## Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and configuration
├── README.md                # This file
├── routers/                 # Tests for API endpoints
│   ├── __init__.py
│   └── test_companies.py    # Tests for company endpoints
├── services/                # Tests for service layer (to be added)
└── utils/                   # Tests for utilities (to be added)
```

## Running Tests

### Install Dependencies

First, install the testing dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/routers/test_companies.py

# Run specific test class
pytest tests/routers/test_companies.py::TestGetTopCompanies

# Run specific test
pytest tests/routers/test_companies.py::TestGetTopCompanies::test_get_top_companies_with_default_parameters
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Coverage

After running tests with coverage (`pytest --cov`), you can view:

- **Terminal report**: Shows coverage percentage for each file
- **HTML report**: Open `htmlcov/index.html` in your browser for detailed coverage
- **XML report**: `coverage.xml` for CI/CD integration

## Writing Tests

### Test Structure

Follow the Arrange-Act-Assert pattern:

```python
def test_example(mock_db_session):
    # Arrange: Set up test data and mocks
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = [{"name": "test"}]
    mock_db_session.execute.return_value = mock_result
    
    # Act: Call the function being tested
    result = function_under_test(db=mock_db_session)
    
    # Assert: Verify the results
    assert result == [{"name": "test"}]
```

### Available Fixtures

- `mock_db_session`: Mock SQLAlchemy database session
- `mock_db_result`: Mock database query result
- `sample_company_data`: Sample company data for testing
- `sample_job_platforms`: Sample job platform names
- `mock_get_job_platforms`: Mocked get_job_platforms function
- `mock_get_job_platforms_empty`: Mocked empty get_job_platforms

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

Use descriptive names that explain what is being tested:
```python
def test_get_top_companies_with_date_filters()
def test_get_top_companies_invalid_limit_too_low()
def test_get_top_companies_database_error()
```

## Best Practices

1. **Test one thing at a time**: Each test should verify one specific behavior
2. **Use descriptive names**: Test names should explain what they test
3. **Mock external dependencies**: Use mocks for database, APIs, etc.
4. **Test edge cases**: Invalid inputs, empty results, boundary values
5. **Test error handling**: Ensure errors are handled gracefully
6. **Keep tests independent**: Tests should not depend on each other
7. **Use fixtures**: Share common setup code via fixtures

## Example Test Cases for get_top_companies

The `test_companies.py` file includes comprehensive tests for the `get_top_companies` endpoint:

### Valid Input Tests
- Default parameters
- Custom limit
- Date filters
- Company name filter
- Remote job filter
- Seniority filter
- Position query filter
- All filters combined
- Empty string filters

### Error Handling Tests
- Database errors
- Unexpected errors

## Continuous Integration

Tests are automatically run in CI/CD pipelines. Ensure all tests pass before merging:

```bash
# Run full test suite with coverage
pytest --cov=app --cov-fail-under=80
```

## Future Additions

- Integration tests with test database
- Performance tests
- API endpoint tests using TestClient
- Additional endpoint tests for other company routes

