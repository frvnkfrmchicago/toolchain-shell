# ToolChain

**AI-powered developer assistant with multi-agent orchestration and RAG**

[![Live Site](https://img.shields.io/badge/live-site-brightgreen)](https://toolchain.vercel.app)
[![Next.js](https://img.shields.io/badge/Next.js-16.1.1-black)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19.2.3-61DAFB)](https://react.dev)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-purple)](https://langchain-ai.github.io/langgraph)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB)](https://python.org)

ToolChain helps developers discover AI tools through a conversational interface powered by a multi-agent LangGraph workflow with RAG-based retrieval.

🔗 **https://toolchain.vercel.app**

[Architecture](#architecture) | [Tech Stack](#tech-stack) | [Getting Started](#getting-started)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER QUERY                               │
│                    "Best vector databases?"                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SUPERVISOR AGENT                           │
│              Routes to specialist agents                        │
│         (OpenAI gpt-4o-mini with structured output)            │
└─────────────────────┬───────────────────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ SEARCH  │ │   RAG   │ │ EXPLAIN │
    │ Agent   │ │  Agent  │ │  Agent  │
    │ (Tavily)│ │ (Chroma)│ │  (LLM)  │
    └─────────┘ └─────────┘ └─────────┘
          │           │           │
          └───────────┴───────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FINAL RESPONSE                               │
│           Structured markdown with recommendations              │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

| Agent | Purpose | Technology |
|-------|---------|------------|
| **Supervisor** | Routes queries to specialists using structured output | OpenAI + Pydantic |
| **RAG** | Retrieves tool info from vector database | ChromaDB + OpenAI embeddings |
| **Search** | Gets latest web info for current events | Tavily API |
| **Explain** | Synthesizes final response with context-aware formatting | OpenAI/Groq LLM |

---

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| **Frontend** | Next.js | 16.1.1 |
| **Frontend** | React | 19.2.3 |
| **Styling** | Tailwind CSS | 4.0 |
| **Animation** | Framer Motion, GSAP | Latest |
| **Backend** | FastAPI | 0.115+ |
| **Orchestration** | LangGraph | 0.2+ |
| **LLM Framework** | LangChain | 0.3+ |
| **Vector DB** | ChromaDB | 1.0+ |
| **Embeddings** | OpenAI | text-embedding-3-small |
| **Search** | Tavily | API |
| **Validation** | Pydantic + Zod | Latest |
| **Logging** | structlog | JSON format |
| **Monitoring** | Prometheus, Sentry | Latest |

---

## Key Files

| File | Purpose |
|------|---------|
| `backend/src/agents/supervisor.py` | Multi-agent routing with structured LLM output |
| `backend/src/agents/workflow.py` | LangGraph StateGraph with conditional edges |
| `backend/src/database/vectorstore.py` | RAG pipeline with ChromaDB + embeddings |
| `backend/src/api/main.py` | FastAPI with SSE streaming endpoint |
| `backend/src/agents/explain_agent.py` | Context-aware response synthesis |
| `frontend/src/app/ask/page.tsx` | Real-time chat with streaming responses |

---

## What This Demonstrates

- **Multi-Agent Orchestration** — Supervisor pattern routes to specialized agents
- **RAG Pipeline** — Vector embeddings with semantic search
- **Streaming Responses** — Real-time SSE for chat UX
- **Context Engineering** — Structured prompts, conversation history
- **LangGraph Workflows** — Production-grade stateful agent loops
- **Bounded Autonomy** — Max iteration limits, graceful fallbacks
- **Structured Output** — Pydantic schemas for LLM responses

---

## Project Structure

```
toolchain/
├── backend/                    # FastAPI + LangGraph
│   ├── src/
│   │   ├── agents/            # LangGraph agent implementations
│   │   │   ├── supervisor.py  # Query routing logic
│   │   │   ├── rag_agent.py   # Vector retrieval
│   │   │   ├── search_agent.py # Web search
│   │   │   ├── explain_agent.py # Response synthesis
│   │   │   ├── workflow.py    # LangGraph wiring
│   │   │   └── llm.py         # LLM provider helpers
│   │   ├── api/               # FastAPI routes
│   │   ├── database/          # ChromaDB vectorstore
│   │   ├── data/              # Seed data (AI tools catalog)
│   │   └── models/            # Pydantic schemas
│   └── tests/                 # pytest tests
│
└── frontend/                   # Next.js 16 + React 19
    └── src/
        ├── app/               # App router pages
        │   ├── ask/           # Conversational interface
        │   └── tools/         # Tool browsing
        └── components/        # UI components
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+ or Bun
- OpenAI API key (required for embeddings)

### Frontend

```bash
cd frontend
bun install
bun dev
```

### Backend

```bash
cd backend
cp .env.example .env  # Add your API keys
uv sync
uv run uvicorn src.api.main:app --reload
```

Open [http://localhost:3000](http://localhost:3000) and ask about AI tools.

---

## Environment Variables

### Backend

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | For embeddings (text-embedding-3-small) |
| `GROQ_API_KEY` | Recommended | LLM fallback (faster, free tier) |
| `TAVILY_API_KEY` | Optional | Web search capability |
| `LANGCHAIN_API_KEY` | Optional | LangSmith tracing |
| `SENTRY_DSN` | Optional | Error tracking |

### Frontend

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend URL (default: http://localhost:8000) |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check + LLM status |
| `GET` | `/api/tools` | List tools with filters |
| `GET` | `/api/tools/{id}` | Get tool details |
| `POST` | `/api/query` | Query agents (non-streaming) |
| `POST` | `/api/query/stream` | Query agents (SSE streaming) |
| `GET` | `/metrics` | Prometheus metrics |

---

## Deployment

### Backend → Railway

```bash
railway login
railway link
railway up
```

### Frontend → Vercel

```bash
cd frontend
vercel
```

Set `NEXT_PUBLIC_API_URL` to your Railway backend URL.

---

## Engineered By

**Frank Lawrence Jr.** — AI Product Engineer & System Architect

- LinkedIn: [linkedin.com/in/franklawrencejr](https://linkedin.com/in/franklawrencejr)
- GitHub: [github.com/franklawrencejr](https://github.com/franklawrencejr)
