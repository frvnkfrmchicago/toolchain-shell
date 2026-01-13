"""Rate limiting middleware for ToolChain API."""

import time

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse
import structlog

from src.config import settings
from src.metrics import record_rate_limit

log = structlog.get_logger()


def _rate_limit_key_func(request: Request) -> str:
    """Get the client identifier for rate limiting.
    
    Uses X-Forwarded-For header if available (for reverse proxies),
    otherwise falls back to remote address.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Get the first IP in the chain (original client)
        return forwarded.split(",")[0].strip()
    return get_remote_address(request)


# Create the limiter instance
limiter = Limiter(
    key_func=_rate_limit_key_func,
    default_limits=[f"{settings.rate_limit_per_minute}/minute"],
    storage_uri=settings.redis_url,  # Use Redis in production; memory:// for local/dev
)


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Custom handler for rate limit exceeded errors.
    
    Returns a JSON response with proper headers for clients to handle rate limiting.
    """
    retry_after_seconds = _get_retry_after_seconds(exc)
    reset_at = int(time.time() + retry_after_seconds)

    log.warning(
        "rate_limit_exceeded",
        client=_rate_limit_key_func(request),
        path=request.url.path,
        limit=exc.detail,
    )

    record_rate_limit(request.url.path)
    
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded",
            "message": f"Rate limit exceeded: {exc.detail}",
            "retry_after": f"{retry_after_seconds} seconds",
        },
        headers={
            "Retry-After": str(retry_after_seconds),
            "X-RateLimit-Limit": str(settings.rate_limit_per_minute),
            "X-RateLimit-Reset": str(reset_at),
        },
    )


def _get_retry_after_seconds(exc: RateLimitExceeded) -> int:
    """Best-effort retry-after calculation for rate limit responses."""
    retry_after = getattr(exc, "retry_after", None)
    if isinstance(retry_after, (int, float)):
        return max(1, int(retry_after))

    reset_at = getattr(exc, "reset_at", None)
    if hasattr(reset_at, "timestamp"):
        return max(1, int(reset_at.timestamp() - time.time()))

    return 60


# Rate limit decorators for specific endpoints
# Query endpoints: 10/minute (more restrictive due to LLM costs)
query_limit = limiter.limit("10/minute")

# Tool listing endpoints: 30/minute
tools_limit = limiter.limit("30/minute")

# Subscribe endpoint: 5/minute (prevent spam)
subscribe_limit = limiter.limit("5/minute")
