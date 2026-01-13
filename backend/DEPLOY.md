# Deploying ToolChain Backend

Per `skills-library-v2/agents/deployment/SKILL.md`

## Platform Recommendation

| Platform | Best For | Why ToolChain Uses It |
|----------|----------|----------------------|
| **Railway** | Full-stack + databases | Persistent storage for ChromaDB, easy env vars |
| Fly.io | Docker, edge | Alternative if you need more regions |
| Render | Simple deployments | Good free tier |

## Railway Deployment (Recommended)

### Prerequisites

1. [Railway account](https://railway.app)
2. GitHub repository with the backend code
3. API keys ready (Groq, OpenAI, optionally Tavily)

### Step-by-Step

#### 1. Create Project

```bash
# Option A: From GitHub
# 1. Go to railway.app
# 2. Click "New Project" → "Deploy from GitHub repo"
# 3. Select your repository
# 4. Select the backend directory

# Option B: CLI
npm install -g @railway/cli
railway login
railway init
railway up
```

#### 2. Configure Environment Variables

In Railway dashboard → Variables, add:

| Variable | Required | Example |
|----------|----------|---------|
| `GROQ_API_KEY` | Yes | `gsk_...` |
| `OPENAI_API_KEY` | Yes | `sk-...` |
| `TAVILY_API_KEY` | No | `tvly_...` |
| `CORS_ORIGINS` | Yes | `https://toolchain.vercel.app` |
| `CHROMA_PERSIST_PATH` | Yes | `/data/chroma_db` |
| `LOG_LEVEL` | No | `INFO` |

#### 3. Add Persistent Volume

ChromaDB needs persistent storage:

1. In Railway dashboard → your service
2. Click "New" → "Volume"
3. Mount path: `/data`
4. This stores your vector database between deploys

#### 4. Verify Deployment

```bash
# Check health endpoint
curl https://your-app.railway.app/health

# Expected response:
# {"status":"healthy","version":"0.1.0"}
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named src" | Ensure `railway.toml` startCommand is correct |
| CORS errors | Add frontend URL to `CORS_ORIGINS` |
| ChromaDB errors | Verify volume is mounted at `/data` |
| Slow cold starts | Railway sleeps after inactivity on free tier |

## Environment Variable Reference

```bash
# Required
GROQ_API_KEY=gsk_...          # LLM for agents
OPENAI_API_KEY=sk_...         # Embeddings
CORS_ORIGINS=https://...      # Frontend URL

# Storage
CHROMA_PERSIST_PATH=/data/chroma_db  # Railway volume path

# Optional
TAVILY_API_KEY=tvly_...       # Web search
LANGCHAIN_TRACING_V2=true     # LangSmith tracing
LANGCHAIN_API_KEY=lsv2_...    # LangSmith key
LOG_LEVEL=INFO                # DEBUG, INFO, WARNING, ERROR
```

## Pre-Deploy Checklist

Per `agents/deployment/SKILL.md`:

```
□ All environment variables documented
□ CORS_ORIGINS set to production frontend URL
□ Health endpoint working (/health)
□ Volume mounted for ChromaDB
□ Secrets rotated if compromised
□ No hardcoded URLs in code
```

## Post-Deploy Checklist

```
□ Health check passing
□ Can query /api/query endpoint
□ CORS working from frontend
□ ChromaDB indexed (check logs for "vectorstore_ready")
□ No errors in Railway logs
```

## Rolling Back

```bash
# Railway CLI
railway rollback

# Or in dashboard:
# Deployments → Select previous → "Rollback"
```

## Local Development

```bash
# Install dependencies
cd backend
uv sync

# Copy env file
cp .env.example .env
# Edit .env with your keys

# Run server
uv run uvicorn src.api.main:app --reload --port 8000

# Test health
curl http://localhost:8000/health
```
