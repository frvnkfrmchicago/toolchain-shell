"""Prometheus metrics for ToolChain observability."""

from prometheus_client import Counter, Histogram, Gauge, Info, REGISTRY, generate_latest
from prometheus_client.core import CollectorRegistry
import time
from functools import wraps
from typing import Callable

import structlog

log = structlog.get_logger()


# Application info
app_info = Info(
    'toolchain_app',
    'ToolChain application info'
)
app_info.info({
    'version': '0.1.0',
    'name': 'toolchain-backend',
})


# Query metrics
query_counter = Counter(
    'toolchain_queries_total',
    'Total number of queries processed',
    ['agent', 'status']
)

query_duration = Histogram(
    'toolchain_query_duration_seconds',
    'Query processing time in seconds',
    ['agent'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Active queries gauge
active_queries = Gauge(
    'toolchain_active_queries',
    'Number of currently processing queries'
)

# Cache metrics
cache_hits = Counter(
    'toolchain_cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

cache_misses = Counter(
    'toolchain_cache_misses_total',
    'Total cache misses',
    ['cache_type']
)

# Rate limit metrics
rate_limit_exceeded = Counter(
    'toolchain_rate_limit_exceeded_total',
    'Number of rate limit exceeded responses',
    ['endpoint']
)

# Error metrics
errors_total = Counter(
    'toolchain_errors_total',
    'Total number of errors',
    ['error_type', 'agent']
)


def track_query(agent: str):
    """Decorator to track query metrics.
    
    Args:
        agent: Name of the agent being tracked
    
    Example:
        @track_query("rag")
        async def rag_agent(state):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            active_queries.inc()
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                query_counter.labels(agent=agent, status='success').inc()
                return result
            except Exception as e:
                query_counter.labels(agent=agent, status='error').inc()
                errors_total.labels(error_type=type(e).__name__, agent=agent).inc()
                raise
            finally:
                duration = time.time() - start_time
                query_duration.labels(agent=agent).observe(duration)
                active_queries.dec()
        
        return wrapper
    return decorator


def get_metrics() -> bytes:
    """Generate Prometheus metrics output.
    
    Returns:
        Prometheus-formatted metrics as bytes
    """
    return generate_latest(REGISTRY)


def record_cache_hit(cache_type: str = "default"):
    """Record a cache hit."""
    cache_hits.labels(cache_type=cache_type).inc()


def record_cache_miss(cache_type: str = "default"):
    """Record a cache miss."""
    cache_misses.labels(cache_type=cache_type).inc()


def record_rate_limit(endpoint: str):
    """Record a rate limit exceeded event."""
    rate_limit_exceeded.labels(endpoint=endpoint).inc()
