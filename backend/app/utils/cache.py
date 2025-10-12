import logging
import time
from functools import wraps
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class SimpleCache:
    """Simple in-memory cache for query results"""

    def __init__(self, default_ttl: int = 300):  # 5 minutes default
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry["expires_at"]:
                return entry["value"]
            else:
                # Remove expired entry
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL"""
        ttl = ttl or self.default_ttl
        self._cache[key] = {"value": value, "expires_at": time.time() + ttl}

    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()

    def size(self) -> int:
        """Get number of cache entries"""
        return len(self._cache)


# Global cache instance
query_cache = SimpleCache()


def cache_result(ttl: int = 300, key_prefix: str = ""):
    """Decorator to cache function results"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = (
                f"{key_prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            )

            # Try to get from cache first
            cached_result = query_cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result

            # Execute function and cache result
            result = func(*args, **kwargs)
            query_cache.set(cache_key, result, ttl)
            logger.debug(f"Cache miss for {cache_key}, cached result")

            return result

        return wrapper

    return decorator
