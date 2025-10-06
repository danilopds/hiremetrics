"""
Unit tests for SecureQueryBuilder utility class

Tests input validation methods to ensure:
- Proper validation of different input types
- SQL injection prevention
- Correct error messages
- Boundary value handling
"""

from datetime import datetime

import pytest
from app.utils.query_builder import SecureQueryBuilder


class TestValidateIntegerInput:
    """Test suite for validate_integer_input method"""

    def test_validate_integer_input_with_valid_int(self):
        """Test validation with valid integer"""
        result = SecureQueryBuilder.validate_integer_input(20, "limit", 1, 100)
        assert result == 20

    def test_validate_integer_input_with_valid_string(self):
        """Test validation with valid string representation of integer"""
        result = SecureQueryBuilder.validate_integer_input("50", "limit", 1, 100)
        assert result == 50

    def test_validate_integer_input_minimum_boundary(self):
        """Test validation at minimum boundary"""
        result = SecureQueryBuilder.validate_integer_input(1, "limit", 1, 100)
        assert result == 1

    def test_validate_integer_input_maximum_boundary(self):
        """Test validation at maximum boundary"""
        result = SecureQueryBuilder.validate_integer_input(100, "limit", 1, 100)
        assert result == 100

    def test_validate_integer_input_below_minimum(self):
        """Test that value below minimum raises ValueError"""
        with pytest.raises(ValueError, match="limit must be at least 1"):
            SecureQueryBuilder.validate_integer_input(0, "limit", 1, 100)

    def test_validate_integer_input_above_maximum(self):
        """Test that value above maximum raises ValueError"""
        with pytest.raises(ValueError, match="limit must be at most 100"):
            SecureQueryBuilder.validate_integer_input(150, "limit", 1, 100)

    def test_validate_integer_input_invalid_string(self):
        """Test that non-numeric string raises ValueError"""
        with pytest.raises(ValueError, match="limit must be a valid integer"):
            SecureQueryBuilder.validate_integer_input("abc", "limit", 1, 100)

    def test_validate_integer_input_invalid_type(self):
        """Test that invalid type raises ValueError"""
        with pytest.raises(ValueError, match="limit must be an integer"):
            SecureQueryBuilder.validate_integer_input([], "limit", 1, 100)


class TestValidateDateInput:
    """Test suite for validate_date_input method"""

    def test_validate_date_input_valid_date(self):
        """Test validation with valid date"""
        result = SecureQueryBuilder.validate_date_input("2024-01-01", "date_from")
        assert result == "2024-01-01"

    def test_validate_date_input_leap_year(self):
        """Test validation with leap year date"""
        result = SecureQueryBuilder.validate_date_input("2024-02-29", "date")
        assert result == "2024-02-29"

    def test_validate_date_input_invalid_format_slashes(self):
        """Test that wrong format with slashes raises ValueError"""
        with pytest.raises(ValueError, match="must be in YYYY-MM-DD format"):
            SecureQueryBuilder.validate_date_input("2024/01/01", "date_from")

    def test_validate_date_input_invalid_format_dots(self):
        """Test that wrong format with dots raises ValueError"""
        with pytest.raises(ValueError, match="must be in YYYY-MM-DD format"):
            SecureQueryBuilder.validate_date_input("2024.01.01", "date_from")

    def test_validate_date_input_invalid_month(self):
        """Test that invalid month raises ValueError"""
        with pytest.raises(ValueError, match="is not a valid date"):
            SecureQueryBuilder.validate_date_input("2024-13-01", "date_from")

    def test_validate_date_input_invalid_day(self):
        """Test that invalid day raises ValueError"""
        with pytest.raises(ValueError, match="is not a valid date"):
            SecureQueryBuilder.validate_date_input("2024-02-30", "date_from")

    def test_validate_date_input_non_leap_year(self):
        """Test that Feb 29 in non-leap year raises ValueError"""
        with pytest.raises(ValueError, match="is not a valid date"):
            SecureQueryBuilder.validate_date_input("2023-02-29", "date_from")

    def test_validate_date_input_not_string(self):
        """Test that non-string input raises ValueError"""
        with pytest.raises(ValueError, match="must be a string"):
            SecureQueryBuilder.validate_date_input(20240101, "date_from")


class TestValidateBooleanInput:
    """Test suite for validate_boolean_input method"""

    def test_validate_boolean_input_string_true_lowercase(self):
        """Test validation with 'true' string"""
        result = SecureQueryBuilder.validate_boolean_input("true", "is_remote")
        assert result is True

    def test_validate_boolean_input_string_true_uppercase(self):
        """Test validation with 'TRUE' string"""
        result = SecureQueryBuilder.validate_boolean_input("TRUE", "is_remote")
        assert result is True

    def test_validate_boolean_input_string_false_lowercase(self):
        """Test validation with 'false' string"""
        result = SecureQueryBuilder.validate_boolean_input("false", "is_remote")
        assert result is False

    def test_validate_boolean_input_string_one(self):
        """Test validation with '1' string"""
        result = SecureQueryBuilder.validate_boolean_input("1", "is_remote")
        assert result is True

    def test_validate_boolean_input_string_zero(self):
        """Test validation with '0' string"""
        result = SecureQueryBuilder.validate_boolean_input("0", "is_remote")
        assert result is False

    def test_validate_boolean_input_actual_boolean_true(self):
        """Test validation with actual boolean True"""
        result = SecureQueryBuilder.validate_boolean_input(True, "is_remote")
        assert result is True

    def test_validate_boolean_input_actual_boolean_false(self):
        """Test validation with actual boolean False"""
        result = SecureQueryBuilder.validate_boolean_input(False, "is_remote")
        assert result is False

    def test_validate_boolean_input_invalid_string(self):
        """Test that invalid string raises ValueError"""
        with pytest.raises(ValueError, match="must be true/false"):
            SecureQueryBuilder.validate_boolean_input("yes", "is_remote")

    def test_validate_boolean_input_invalid_type(self):
        """Test that invalid type raises ValueError"""
        with pytest.raises(ValueError, match="must be a string or boolean"):
            SecureQueryBuilder.validate_boolean_input(1, "is_remote")


class TestValidateTextInput:
    """Test suite for validate_text_input method"""

    def test_validate_text_input_valid_company_name(self):
        """Test validation with valid company name"""
        result = SecureQueryBuilder.validate_text_input("Tech Corp", "company")
        assert result == "Tech Corp"

    def test_validate_text_input_with_special_chars(self):
        """Test validation with allowed special characters"""
        result = SecureQueryBuilder.validate_text_input(
            "O'Reilly & Associates", "company"
        )
        assert result == "O'Reilly & Associates"

    def test_validate_text_input_with_unicode(self):
        """Test validation with Unicode characters (accents, etc.)"""
        result = SecureQueryBuilder.validate_text_input("Société Générale", "company")
        assert result == "Société Générale"

    def test_validate_text_input_strips_whitespace(self):
        """Test that leading/trailing whitespace is stripped"""
        result = SecureQueryBuilder.validate_text_input("  Tech Corp  ", "company")
        assert result == "Tech Corp"

    def test_validate_text_input_sql_injection_drop_table(self):
        """Test that SQL DROP TABLE injection is blocked"""
        with pytest.raises(ValueError, match="Invalid input detected"):
            SecureQueryBuilder.validate_text_input(
                "'; DROP TABLE companies; --", "company"
            )

    def test_validate_text_input_sql_injection_union_select(self):
        """Test that UNION SELECT injection is blocked"""
        with pytest.raises(ValueError, match="Invalid input detected"):
            SecureQueryBuilder.validate_text_input(
                "' UNION SELECT * FROM users --", "company"
            )

    def test_validate_text_input_sql_injection_or_1_equals_1(self):
        """Test that OR 1=1 injection is blocked"""
        with pytest.raises(ValueError, match="Invalid input detected"):
            SecureQueryBuilder.validate_text_input("admin' OR 1=1 --", "company")

    def test_validate_text_input_exceeds_max_length(self):
        """Test that text exceeding max length raises ValueError"""
        long_text = "A" * 256
        with pytest.raises(ValueError, match="exceeds maximum length"):
            SecureQueryBuilder.validate_text_input(long_text, "company", max_length=255)

    def test_validate_text_input_not_string(self):
        """Test that non-string input raises ValueError"""
        with pytest.raises(ValueError, match="must be a string"):
            SecureQueryBuilder.validate_text_input(123, "company")

    def test_validate_text_input_empty_string(self):
        """Test that empty string is valid"""
        result = SecureQueryBuilder.validate_text_input("", "company")
        assert result == ""


class TestValidateListInput:
    """Test suite for validate_list_input method"""

    def test_validate_list_input_with_list(self):
        """Test validation with actual list"""
        result = SecureQueryBuilder.validate_list_input(
            ["skill1", "skill2", "skill3"], "skills"
        )
        assert result == ["skill1", "skill2", "skill3"]

    def test_validate_list_input_with_comma_separated_string(self):
        """Test validation with comma-separated string"""
        result = SecureQueryBuilder.validate_list_input(
            "skill1,skill2,skill3", "skills"
        )
        assert result == ["skill1", "skill2", "skill3"]

    def test_validate_list_input_strips_whitespace(self):
        """Test that whitespace around items is stripped"""
        result = SecureQueryBuilder.validate_list_input(
            " skill1 , skill2 , skill3 ", "skills"
        )
        assert result == ["skill1", "skill2", "skill3"]

    def test_validate_list_input_exceeds_max_items(self):
        """Test that exceeding max items raises ValueError"""
        items = [f"item{i}" for i in range(101)]
        with pytest.raises(ValueError, match="cannot have more than 100 items"):
            SecureQueryBuilder.validate_list_input(items, "skills", max_items=100)

    def test_validate_list_input_with_sql_injection_in_item(self):
        """Test that SQL injection in list items is blocked"""
        with pytest.raises(ValueError, match="Invalid input detected"):
            SecureQueryBuilder.validate_list_input(
                ["skill1", "'; DROP TABLE skills; --"], "skills"
            )

    def test_validate_list_input_invalid_type(self):
        """Test that invalid type raises ValueError"""
        with pytest.raises(
            ValueError, match="must be a list or comma-separated string"
        ):
            SecureQueryBuilder.validate_list_input(123, "skills")

    def test_validate_list_input_with_non_string_items(self):
        """Test that non-string items raise ValueError"""
        with pytest.raises(ValueError, match="All items in skills must be strings"):
            SecureQueryBuilder.validate_list_input([1, 2, 3], "skills")


class TestBuildWhereClause:
    """Test suite for build_where_clause method"""

    def test_build_where_clause_with_single_filter(self):
        """Test building WHERE clause with single filter"""
        filters = {"employer_name": "Tech Corp"}
        where_clause, params = SecureQueryBuilder.build_where_clause(filters)

        assert "WHERE" in where_clause
        assert "employer_name = :param_employer_name" in where_clause
        assert params["param_employer_name"] == "Tech Corp"

    def test_build_where_clause_with_multiple_filters(self):
        """Test building WHERE clause with multiple filters"""
        filters = {"employer_name": "Tech Corp", "seniority": "Senior"}
        where_clause, params = SecureQueryBuilder.build_where_clause(filters)

        assert "WHERE" in where_clause
        assert "AND" in where_clause
        assert "employer_name = :param_employer_name" in where_clause
        assert "seniority = :param_seniority" in where_clause
        assert len(params) == 2

    def test_build_where_clause_ignores_none_values(self):
        """Test that None values are ignored"""
        filters = {"employer_name": "Tech Corp", "seniority": None}
        where_clause, params = SecureQueryBuilder.build_where_clause(filters)

        assert "employer_name = :param_employer_name" in where_clause
        assert "seniority" not in where_clause
        assert len(params) == 1

    def test_build_where_clause_ignores_empty_strings(self):
        """Test that empty strings are ignored"""
        filters = {"employer_name": "Tech Corp", "seniority": ""}
        where_clause, params = SecureQueryBuilder.build_where_clause(filters)

        assert "employer_name = :param_employer_name" in where_clause
        assert "seniority" not in where_clause
        assert len(params) == 1

    def test_build_where_clause_ignores_null_strings(self):
        """Test that 'null' strings are ignored"""
        filters = {"employer_name": "Tech Corp", "seniority": "null"}
        where_clause, params = SecureQueryBuilder.build_where_clause(filters)

        assert "employer_name = :param_employer_name" in where_clause
        assert "seniority" not in where_clause
        assert len(params) == 1

    def test_build_where_clause_with_no_filters(self):
        """Test that empty filters return empty WHERE clause"""
        filters = {}
        where_clause, params = SecureQueryBuilder.build_where_clause(filters)

        assert where_clause == ""
        assert params == {}

    def test_build_where_clause_with_all_none_filters(self):
        """Test that all None filters return empty WHERE clause"""
        filters = {"employer_name": None, "seniority": None}
        where_clause, params = SecureQueryBuilder.build_where_clause(filters)

        assert where_clause == ""
        assert params == {}


# Parametrized tests for common validation scenarios
@pytest.mark.parametrize(
    "value,min_val,max_val,should_pass",
    [
        (1, 1, 100, True),  # Minimum boundary
        (100, 1, 100, True),  # Maximum boundary
        (50, 1, 100, True),  # Middle value
        (0, 1, 100, False),  # Below minimum
        (101, 1, 100, False),  # Above maximum
        (-1, 1, 100, False),  # Negative value
    ],
)
def test_validate_integer_parametrized(value, min_val, max_val, should_pass):
    """Parametrized test for integer validation with various boundary conditions"""
    if should_pass:
        result = SecureQueryBuilder.validate_integer_input(
            value, "test_field", min_val, max_val
        )
        assert result == value
    else:
        with pytest.raises(ValueError):
            SecureQueryBuilder.validate_integer_input(
                value, "test_field", min_val, max_val
            )


@pytest.mark.parametrize(
    "sql_injection,description",
    [
        ("'; DROP TABLE users; --", "DROP TABLE with comment"),
        ("' OR '1'='1", "OR 1=1 injection"),
        ("' UNION SELECT * FROM passwords --", "UNION SELECT"),
        ("admin'--", "Comment-based injection"),
        ("' AND 1=1 --", "AND 1=1 injection"),
        ("'; DELETE FROM users WHERE '1'='1", "DELETE with WHERE"),
        ("' OR 1=1; --", "OR with semicolon"),
        ("' EXEC sp_executesql --", "EXEC command"),
    ],
)
def test_sql_injection_attempts_parametrized(sql_injection, description):
    """Parametrized test for various SQL injection attempts"""
    with pytest.raises(ValueError, match="Invalid input detected"):
        SecureQueryBuilder.validate_text_input(sql_injection, "test_field")
