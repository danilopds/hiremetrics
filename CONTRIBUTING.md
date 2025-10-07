# Contributing to HireMetrics

Thank you for your interest in contributing to HireMetrics! We welcome contributions from the community and appreciate your effort to make this project better.

## Table of Contents

- [How to Report Issues](#how-to-report-issues)
- [How to Submit Pull Requests](#how-to-submit-pull-requests)
- [Coding Style Guidelines](#coding-style-guidelines)
- [Running Tests](#running-tests)
- [Review Process and Expectations](#review-process-and-expectations)
- [Community](#community)

---

## How to Report Issues

Use GitHub Issues to track bugs and feature requests. Before creating an issue, search existing issues and verify you're using the latest version.

### Bug Reports

Include:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python/Node version, browser)
- Screenshots or logs if applicable

### Feature Requests

Include:
- Problem you're solving
- Proposed solution
- Use case and benefits to HireMetrics users

---

## How to Submit Pull Requests

We actively welcome your pull requests! Follow these steps:

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/hiremetrics.git
cd hiremetrics

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/hiremetrics.git
```

### 2. Create a Feature Branch

```bash
# Update your fork with the latest changes
git fetch upstream
git checkout main
git merge upstream/main

# Create a new branch for your feature
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Write clear, concise commit messages
- Follow the [coding style guidelines](#coding-style-guidelines)
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic


### 4. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Go to GitHub and create a Pull Request
```

### Pull Request Guidelines

- **Title**: Use a clear, descriptive title
- **Description**: Explain what changes you made and why
- **Link related issues**: Use keywords like "Fixes #123" or "Closes #456"
- **Screenshots**: Include screenshots for UI changes
- **Breaking changes**: Clearly mark any breaking changes
- **Keep it focused**: One feature/fix per PR when possible

---

## Coding Style Guidelines

We maintain consistent code style across the project to ensure readability and maintainability.

### Python (Backend & ETL)

We use **Black** and **isort** for automatic code formatting:

- **Black version**: `25.9.0`
- **isort version**: `6.1.0` with `--profile black`

#### Formatting Your Code

```bash
# Format backend code
black ./backend
isort --profile black --filter-files ./backend

# Format ETL code
black ./etl
isort --profile black --filter-files ./etl
```

**Best practices:**
- Follow PEP 8 (enforced by Black)
- Use type hints and docstrings
- Keep functions focused and concise
- Use meaningful names

### JavaScript/Vue (Frontend)

Use **ESLint** for code linting:

```bash
# Lint frontend code
cd frontend
npm run lint
```

**Best practices:**
- Follow **Vue 3 Composition API** with `<script setup>` syntax
- Use **ESLint** configuration provided
- Use **Tailwind CSS** utility classes
- Use **Pinia stores** for state management
- Keep components focused and reusable

---

## Running Tests

We maintain comprehensive test suites to ensure code quality and prevent regressions.

### Backend Tests

Our backend tests are located in `backend/tests/` and use **pytest**.

#### Test Structure

```
backend/tests/
├── conftest.py              # Pytest fixtures and configuration
├── routers/                 # Tests for API endpoints
│   ├── test_companies.py
│   ├── test_auth.py
│   └── test_skills.py
└── utils/                   # Tests for utility functions
    ├── test_auth.py
    └── test_query_builder.py
```

#### Running Tests Locally

```bash
cd backend
pip install -r requirements.txt

# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/routers/test_companies.py
```

#### Writing Tests

Follow the **Arrange-Act-Assert** pattern:

```python
def test_get_top_companies_with_filters(mock_db_session):
    # Arrange: Set up test data and mocks
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = [
        {"company_name": "Test Corp", "job_count": 100}
    ]
    mock_db_session.execute.return_value = mock_result
    
    # Act: Call the function being tested
    result = get_top_companies(db=mock_db_session, limit=10)
    
    # Assert: Verify the results
    assert len(result) == 1
    assert result[0]["company_name"] == "Test Corp"
```

### CI/CD Workflows

GitHub Actions workflows in `.github/workflows/` automatically run on push/PR to `main`:

1. **`backend-pytest.yml`** - Runs all backend tests with Python 3.11
2. **`code-formatting.yml`** - Checks backend/ETL code formatting with Black and isort
3. **`frontend-lint.yml`** - Runs ESLint checks on frontend code

**All tests and linting checks must pass before merging.**

---

## Review Process and Expectations

### Timeline

- **Initial response**: Within 2-3 business days
- **Review**: Maintainers will evaluate functionality, code quality, tests, and documentation
- **Iteration**: Address feedback as needed
- **Merge**: Once approved and all checks pass

### Review Criteria

- ✅ **Code Quality** - Follows style guidelines, well-documented, clear naming
- ✅ **Testing** - Includes tests for new features, existing tests pass
- ✅ **Documentation** - Updated as needed (README, docstrings)
- ✅ **Automated Checks** - All GitHub Actions workflows pass

### Tips for Faster Reviews

- Keep PRs small and focused
- Write clear descriptions explaining what and why
- Respond promptly to feedback
- Be receptive to suggestions

---

## Community

### Getting Help

- 💬 **Discord**: Join our community at [https://discord.gg/rr7TkzzR](https://discord.gg/rr7TkzzR) for discussions and questions
- 📖 **Documentation**: Check README.md and backend/tests/README.md
- 💡 **GitHub Discussions**: For feature discussions and general questions
- 🐛 **GitHub Issues**: For bug reports and feature requests

---

## Code of Conduct

Please note that this project follows a standard code of conduct. By participating, you agree to:

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

---

Thank you for contributing to HireMetrics! 🚀
