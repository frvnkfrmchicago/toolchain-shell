"""In-memory caching layer for ToolChain API."""

import hashlib
import json
import time
from functools import wraps
from typing import Any, Callable, Optional

import structlog

from src.metrics import record_cache_hit, record_cache_miss

log = structlog.get_logger()


class SimpleCache:
    """Simple in-memory cache with TTL support.
    
    For production with multiple workers, upgrade to Redis.
    """

    def __init__(self, default_ttl: int = 3600):
        """Initialize cache.
        
        Args:
            default_ttl: Default time-to-live in seconds (1 hour)
        """
        self._cache: dict[str, tuple[Any, float]] = {}
        self._default_ttl = default_ttl

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate a cache key from arguments."""
        key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        hash_digest = hashlib.md5(key_data.encode()).hexdigest()
        return f"{prefix}:{hash_digest}"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key not in self._cache:
            return None
        
        value, expires_at = self._cache[key]
        
        if time.time() > expires_at:
            # Expired, remove and return None
            del self._cache[key]
            log.debug("cache_expired", key=key[:50])
            return None
        
        log.debug("cache_hit", key=key[:50])
        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL."""
        ttl = ttl or self._default_ttl
        expires_at = time.time() + ttl
        self._cache[key] = (value, expires_at)
        log.debug("cache_set", key=key[:50], ttl=ttl)

    def delete(self, key: str) -> bool:
        """Delete a key from cache."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all cached data."""
        self._cache.clear()
        log.info("cache_cleared")

    def cleanup_expired(self) -> int:
        """Remove expired entries. Returns count of removed entries."""
        now = time.time()
        expired_keys = [
            key for key, (_, expires_at) in self._cache.items()
            if now > expires_at
        ]
        for key in expired_keys:
            del self._cache[key]
        
        if expired_keys:
            log.info("cache_cleanup", removed=len(expired_keys))
        
        return len(expired_keys)


# Global cache instance
cache = SimpleCache()


def cached(prefix: str, ttl: Optional[int] = None):
    """Decorator to cache function results.
    
    Args:
        prefix: Prefix for cache keys (e.g., 'tool_query')
        ttl: Time-to-live in seconds (defaults to cache default)
    
    Example:
        @cached("tool_query", ttl=3600)
        def get_tools(query: str):
            return search_tools(query)
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = cache._generate_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                record_cache_hit(prefix)
                return result

            record_cache_miss(prefix)
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator


def async_cached(prefix: str, ttl: Optional[int] = None):
    """Decorator to cache async function results.
    
    Args:
        prefix: Prefix for cache keys
        ttl: Time-to-live in seconds
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = cache._generate_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                record_cache_hit(prefix)
                return result

            record_cache_miss(prefix)
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator
