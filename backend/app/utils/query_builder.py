"""
Secure Query Builder for SQL Injection Prevention
Handles parameterized queries and input validation
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import text


class SecureQueryBuilder:
    """Secure query builder to prevent SQL injection attacks"""

    # Allowed characters for text fields (excluding SQL injection patterns)
    # Supports Unicode letters and diacritics for international place names
    SAFE_TEXT_PATTERN = re.compile(
        r'^[\w\s\-_.,@#$%&*()+=!?/:;<>[\]{}|~`"\'\u00C0-\u017F\u0100-\u024F]*$',
        re.UNICODE,
    )

    # Date pattern validation
    DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    # Boolean pattern validation
    BOOLEAN_PATTERN = re.compile(r"^(true|false|1|0)$", re.IGNORECASE)

    # Integer pattern validation
    INTEGER_PATTERN = re.compile(r"^\d+$")

    @staticmethod
    def validate_text_input(value: str, field_name: str, max_length: int = 255) -> str:
        """Validate and sanitize text input"""
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

        if len(value) > max_length:
            raise ValueError(f"{field_name} exceeds maximum length of {max_length}")

        # Check for SQL injection patterns
        sql_patterns = [
            r"(\b(union|select|insert|update|delete|drop|create|alter|exec|execute|script)\b)",
            r"(\b(and|or)\b\s+\d+\s*[=<>])",
            r"(\b(and|or)\b\s+\'[^\']*\'\s*[=<>])",
            r"(\b(and|or)\b\s+\"[^\"]*\"\s*[=<>])",
            r"(\b(and|or)\b\s+true\s*[=<>])",
            r"(\b(and|or)\b\s+false\s*[=<>])",
            r"(\b(and|or)\b\s+null\s*[=<>])",
            r"(\b(and|or)\b\s+1\s*=\s*1)",
            r"(\b(and|or)\b\s+1\s*=\s*2)",
            r"(\b(and|or)\b\s+\d+\s*=\s*\d+)",
            r"(\b(and|or)\b\s+\'[^\']*\'\s*=\s*\'[^\']*\')",
            r"(\b(and|or)\b\s+\"[^\"]*\"\s*=\s*\"[^\"]*\")",
            r"(\b(and|or)\b\s+true\s*=\s*true)",
            r"(\b(and|or)\b\s+false\s*=\s*false)",
            r"(\b(and|or)\b\s+null\s*=\s*null)",
            r"(\b(and|or)\b\s+1\s*=\s*1\s*--)",
            r"(\b(and|or)\b\s+1\s*=\s*2\s*--)",
            r"(\b(and|or)\b\s+\d+\s*=\s*\d+\s*--)",
            r"(\b(and|or)\b\s+\'[^\']*\'\s*=\s*\'[^\']*\'\s*--)",
            r"(\b(and|or)\b\s+\"[^\"]*\"\s*=\s*\"[^\"]*\"\s*--)",
            r"(\b(and|or)\b\s+true\s*=\s*true\s*--)",
            r"(\b(and|or)\b\s+false\s*=\s*false\s*--)",
            r"(\b(and|or)\b\s+null\s*=\s*null\s*--)",
            r"(\b(and|or)\b\s+1\s*=\s*1\s*#)",
            r"(\b(and|or)\b\s+1\s*=\s*2\s*#)",
            r"(\b(and|or)\b\s+\d+\s*=\s*\d+\s*#)",
            r"(\b(and|or)\b\s+\'[^\']*\'\s*=\s*\'[^\']*\'\s*#)",
            r"(\b(and|or)\b\s+\"[^\"]*\"\s*=\s*\"[^\"]*\"\s*#)",
            r"(\b(and|or)\b\s+true\s*=\s*true\s*#)",
            r"(\b(and|or)\b\s+false\s*=\s*false\s*#)",
            r"(\b(and|or)\b\s+null\s*=\s*null\s*#)",
            r"(\b(and|or)\b\s+1\s*=\s*1\s*/\*)",
            r"(\b(and|or)\b\s+1\s*=\s*2\s*/\*)",
            r"(\b(and|or)\b\s+\d+\s*=\s*\d+\s*/\*)",
            r"(\b(and|or)\b\s+\'[^\']*\'\s*=\s*\'[^\']*\'\s*/\*)",
            r"(\b(and|or)\b\s+\"[^\"]*\"\s*=\s*\"[^\"]*\"\s*/\*)",
            r"(\b(and|or)\b\s+true\s*=\s*true\s*/\*)",
            r"(\b(and|or)\b\s+false\s*=\s*false\s*/\*)",
            r"(\b(and|or)\b\s+null\s*=\s*null\s*/\*)",
            r"(\b(and|or)\b\s+1\s*=\s*1\s*\*/)",
            r"(\b(and|or)\b\s+1\s*=\s*2\s*\*/)",
            r"(\b(and|or)\b\s+\d+\s*=\s*\d+\s*\*/)",
            r"(\b(and|or)\b\s+\'[^\']*\'\s*=\s*\'[^\']*\'\s*\*/)",
            r"(\b(and|or)\b\s+\"[^\"]*\"\s*=\s*\"[^\"]*\"\s*\*/)",
            r"(\b(and|or)\b\s+true\s*=\s*true\s*\*/)",
            r"(\b(and|or)\b\s+false\s*=\s*false\s*\*/)",
            r"(\b(and|or)\b\s+null\s*=\s*null\s*\*/)",
            r"(\b(and|or)\b\s+1\s*=\s*1\s*;)",
            r"(\b(and|or)\b\s+1\s*=\s*2\s*;)",
            r"(\b(and|or)\b\s+\d+\s*=\s*\d+\s*;)",
            r"(\b(and|or)\b\s+\'[^\']*\'\s*=\s*\'[^\']*\'\s*;)",
            r"(\b(and|or)\b\s+\"[^\"]*\"\s*=\s*\"[^\"]*\"\s*;)",
            r"(\b(and|or)\b\s+true\s*=\s*true\s*;)",
            r"(\b(and|or)\b\s+false\s*=\s*false\s*;)",
            r"(\b(and|or)\b\s+null\s*=\s*null\s*;)",
            r"(\b(and|or)\b\s+1\s*=\s*1\s*$)",
            r"(\b(and|or)\b\s+1\s*=\s*2\s*$)",
            r"(\b(and|or)\b\s+\d+\s*=\s*\d+\s*$)",
            r"(\b(and|or)\b\s+\'[^\']*\'\s*=\s*\'[^\']*\'\s*$)",
            r"(\b(and|or)\b\s+\"[^\"]*\"\s*=\s*\"[^\"]*\"\s*$)",
            r"(\b(and|or)\b\s+true\s*=\s*true\s*$)",
            r"(\b(and|or)\b\s+false\s*=\s*false\s*$)",
            r"(\b(and|or)\b\s+null\s*=\s*null\s*$)",
        ]

        for pattern in sql_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                raise ValueError(f"Invalid input detected in {field_name}")

        # Additional safety check
        if not SecureQueryBuilder.SAFE_TEXT_PATTERN.match(value):
            raise ValueError(f"Invalid characters in {field_name}")

        return value.strip()

    @staticmethod
    def validate_date_input(value: str, field_name: str) -> str:
        """Validate date input format"""
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

        if not SecureQueryBuilder.DATE_PATTERN.match(value):
            raise ValueError(f"{field_name} must be in YYYY-MM-DD format")

        # Validate actual date
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"{field_name} is not a valid date")

        return value

    @staticmethod
    def validate_boolean_input(value: str, field_name: str) -> bool:
        """Validate boolean input"""
        if isinstance(value, bool):
            return value

        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string or boolean")

        if not SecureQueryBuilder.BOOLEAN_PATTERN.match(value):
            raise ValueError(f"{field_name} must be true/false, 1/0, or True/False")

        return value.lower() in ("true", "1")

    @staticmethod
    def validate_integer_input(
        value: Any,
        field_name: str,
        min_val: Optional[int] = None,
        max_val: Optional[int] = None,
    ) -> int:
        """Validate integer input"""
        if isinstance(value, int):
            result = value
        elif isinstance(value, str):
            if not SecureQueryBuilder.INTEGER_PATTERN.match(value):
                raise ValueError(f"{field_name} must be a valid integer")
            result = int(value)
        else:
            raise ValueError(f"{field_name} must be an integer")

        if min_val is not None and result < min_val:
            raise ValueError(f"{field_name} must be at least {min_val}")

        if max_val is not None and result > max_val:
            raise ValueError(f"{field_name} must be at most {max_val}")

        return result

    @staticmethod
    def validate_list_input(
        value: Any, field_name: str, max_items: int = 100
    ) -> List[str]:
        """Validate list input"""
        if isinstance(value, str):
            # Handle comma-separated string
            items = [item.strip() for item in value.split(",") if item.strip()]
        elif isinstance(value, list):
            items = value
        else:
            raise ValueError(f"{field_name} must be a list or comma-separated string")

        if len(items) > max_items:
            raise ValueError(f"{field_name} cannot have more than {max_items} items")

        # Validate each item
        validated_items = []
        for item in items:
            if not isinstance(item, str):
                raise ValueError(f"All items in {field_name} must be strings")
            validated_items.append(
                SecureQueryBuilder.validate_text_input(item, f"{field_name} item")
            )

        return validated_items

    @staticmethod
    def build_where_clause(filters: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Build a secure WHERE clause with parameters"""
        conditions = []
        params = {}

        for field, value in filters.items():
            if value is not None and value != "" and value != "null":
                param_name = f"param_{field}"
                conditions.append(f"{field} = :{param_name}")
                params[param_name] = value

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        return where_clause, params

    @staticmethod
    def build_secure_query(
        base_query: str, where_clause: str, params: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """Build a secure parameterized query"""
        # Validate base query doesn't contain user input
        if any(char in base_query for char in ["%", "{", "}"]):
            raise ValueError("Base query contains potentially unsafe characters")

        full_query = f"{base_query} {where_clause}"
        return text(full_query), params
