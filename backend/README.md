# ToolChain Backend

AI Tool Discovery Platform - Multi-Agent Backend

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Copy environment file:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the server:
```bash
uv run uvicorn src.api.main:app --reload
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/tools` - List all tools (with optional filters)
- `GET /api/tools/{id}` - Get tool by ID
- `GET /api/categories` - List categories with counts
- `POST /api/compare` - Compare multiple tools
- `POST /api/query` - Query AI agent for recommendations
- `POST /api/query/stream` - Stream query results via SSE
- `POST /api/subscribe` - Email subscription

## Architecture

```
USER QUERY
    |
    v
SUPERVISOR (routes to agents)
    |
    +-- SEARCH (Tavily web search)
    +-- RAG (Chroma vector retrieval)
    +-- EXPLAIN (synthesizes response)
    |
    v
FINAL RESPONSE
```

## Tech Stack

- FastAPI + uvicorn
- LangGraph for workflow orchestration
- LangChain for LLM interactions
- Chroma for vector database
- Tavily for web search
- Pydantic for type validation
- structlog for logging
