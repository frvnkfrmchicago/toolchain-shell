"""FastAPI application for ToolChain backend."""

import json
from contextlib import asynccontextmanager

import structlog
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from slowapi.errors import RateLimitExceeded

from src.api.middleware import (
    limiter,
    rate_limit_exceeded_handler,
    query_limit,
    tools_limit,
    subscribe_limit,
)

from src.agents.workflow import run_query, stream_query
from src.config import settings
from src.metrics import get_metrics
from src.data.seed_tools import (
    get_all_tools,
    get_categories_with_counts,
    get_tool_by_id,
)
from src.database.vectorstore import ensure_indexed
from src.models.tool import ChatQuery, CompareRequest, SubscribeRequest

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)

log = structlog.get_logger()

# Initialize Sentry for error tracking
if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            StarletteIntegration(transaction_style="endpoint"),
        ],
        traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
        environment="production" if not settings.debug else "development",
        send_default_pii=False,
    )
    log.info("sentry_initialized", environment="production" if not settings.debug else "development")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup."""
    log.info("startup", action="initializing")
    
    # Fail fast if required API keys are missing
    if not settings.openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY is required for embeddings. "
            "Set it in .env file. Get key at: https://platform.openai.com/api-keys"
        )
    
    ensure_indexed()
    log.info("startup_complete")
    yield
    log.info("shutdown")


app = FastAPI(
    title="ToolChain API",
    description="AI Tool Discovery Platform - Multi-Agent Backend",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint for monitoring."""
    from fastapi.responses import Response
    return Response(
        content=get_metrics(),
        media_type="text/plain; charset=utf-8"
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    from src.agents.llm import get_llm
    from src.config import settings
    
    # Test LLM availability
    llm_status = "unknown"
    try:
        test_llm = get_llm(temperature=0)
        llm_status = "available"
    except Exception as e:
        llm_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "version": "0.1.0",
        "openai_configured": bool(settings.openai_api_key),
        "groq_configured": bool(settings.groq_api_key),
        "llm_status": llm_status,
    }


@app.get("/api/tools")
@tools_limit
async def list_tools(
    request: Request,
    category: str | None = None,
    pricing: str | None = None,
    language: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
):
    """List all tools with optional filters."""
    tools = get_all_tools()
    
    # Apply filters
    if category:
        tools = [t for t in tools if t.category == category]
    if pricing:
        tools = [t for t in tools if t.pricing == pricing]
    if language:
        tools = [t for t in tools if language.lower() in [l.lower() for l in t.languages]]
    
    # Sort by popularity
    tools = sorted(tools, key=lambda t: t.popularity_score, reverse=True)
    
    # Apply limit
    tools = tools[:limit]
    
    return {"tools": [t.model_dump() for t in tools], "total": len(tools)}


@app.get("/api/tools/{tool_id}")
@tools_limit
async def get_tool(request: Request, tool_id: str):
    """Get a specific tool by ID."""
    tool = get_tool_by_id(tool_id)
    
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")
    
    return tool.model_dump()


@app.get("/api/categories")
@tools_limit
async def list_categories(request: Request):
    """Get all categories with tool counts."""
    counts = get_categories_with_counts()
    
    # Add display names
    category_names = {
        "api": "APIs",
        "mcp": "MCPs",
        "sdk": "SDKs",
        "cli": "CLIs",
        "vector_db": "Vector Databases",
        "framework": "Frameworks",
        "agent_framework": "Agent Frameworks",
    }
    
    categories = [
        {
            "id": cat,
            "name": category_names.get(cat, cat.title()),
            "count": count,
        }
        for cat, count in counts.items()
    ]
    
    return {"categories": categories}


@app.post("/api/compare")
@tools_limit
async def compare_tools(request: Request, data: CompareRequest):
    """Compare multiple tools side by side."""
    tools = []
    
    for tool_id in data.tool_ids:
        tool = get_tool_by_id(tool_id)
        if tool:
            tools.append(tool.model_dump())
        else:
            raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")
    
    return {"tools": tools}


@app.post("/api/query")
@query_limit
async def query_tools(request: Request, query: ChatQuery):
    """Query the AI agent for tool recommendations."""
    log.info("query_start", query=query.query)
    
    result = await run_query(query.query)
    
    return {
        "query": query.query,
        "response": result.get("final_response", "No response generated"),
        "messages": result.get("messages", []),
    }


@app.post("/api/query/stream")
@query_limit
async def stream_query_tools(request: Request, query: ChatQuery):
    """Stream query results via Server-Sent Events."""
    log.info("stream_query_start", query=query.query, has_history=bool(query.messages))

    # Convert Pydantic messages to dicts for state
    conversation_history = [
        {"role": msg.role, "content": msg.content, "timestamp": msg.timestamp}
        for msg in query.messages
    ] if query.messages else []

    async def event_generator():
        try:
            async for event in stream_query(query.query, conversation_history):
                # Format as SSE
                data = json.dumps(event)
                yield f"data: {data}\n\n"
            
            # Send done event
            yield "data: {\"done\": true}\n\n"
        except Exception as e:
            log.error("stream_query_error", error=str(e), traceback=str(e.__traceback__))
            # Send error event
            error_data = json.dumps({
                "error": str(e),
                "node": "error",
                "messages": [f"Error: {str(e)}"],
            })
            yield f"data: {error_data}\n\n"
            yield "data: {\"done\": true}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/api/subscribe")
@subscribe_limit
async def subscribe(request: Request, data: SubscribeRequest):
    """Subscribe to email updates."""
    # Log only domain to protect PII
    email_domain = data.email.split("@")[-1] if "@" in data.email else "invalid"
    log.info("subscribe", email_domain=email_domain)
    
    # In production, store in database or send to email service
    # For now, just log and return success
    
    return {"success": True, "message": "Subscribed successfully"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
