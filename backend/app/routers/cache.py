"""Cache management endpoints"""

from fastapi import APIRouter

from ..utils.cache import query_cache

router = APIRouter()


@router.get("/status")
async def get_cache_status():
    """Get cache status and statistics"""
    return {
        "cache_size": query_cache.size(),
        "cache_enabled": True,
        "default_ttl": query_cache.default_ttl,
    }


@router.post("/clear")
async def clear_cache():
    """Clear all cached data"""
    query_cache.clear()
    return {"message": "Cache cleared successfully"}
