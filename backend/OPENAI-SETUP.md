# Switching to OpenAI API

The Toolchain backend now supports **OpenAI as the primary LLM provider** with Groq as a fallback.

## Quick Setup

### 1. Install Dependencies

Make sure `langchain-openai` is installed:

```bash
cd backend
uv add langchain-openai
```

### 2. Set Your OpenAI API Key

Create a `.env` file in the `backend/` directory (if it doesn't exist):

```bash
cd backend
cp .env.example .env  # If .env.example exists
# OR create .env manually
```

Add your OpenAI API key:

```bash
# .env
OPENAI_API_KEY=sk-your-actual-openai-key-here
```

**Get your OpenAI API key:**
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)
4. Paste it in your `.env` file

### 3. Restart the Server

```bash
uv run uvicorn src.api.main:app --reload
```

## How It Works

The system now:
1. **Tries OpenAI first** (if `OPENAI_API_KEY` is set)
2. **Falls back to Groq** (if OpenAI fails or isn't configured)
3. **Uses `gpt-4o-mini` by default** (fast, cheap OpenAI model)

## Model Selection

You can customize the model by editing the agent files:

```python
# In supervisor.py or explain_agent.py
llm = get_llm(
    model="gpt-4o",  # Use GPT-4o instead of gpt-4o-mini
    temperature=0.7,
)
```

**Available OpenAI models:**
- `gpt-4o-mini` - Fast, cheap (default)
- `gpt-4o` - More capable
- `gpt-4-turbo` - Previous generation
- `gpt-3.5-turbo` - Cheapest option

## Testing

1. Make sure your `.env` file has `OPENAI_API_KEY` set
2. Start the backend: `uv run uvicorn src.api.main:app --reload`
3. Check logs - you should see: `using_openai model=gpt-4o-mini`
4. Try a query in the frontend

## Troubleshooting

### "No LLM API key configured"
- Make sure `.env` file exists in `backend/` directory
- Make sure `OPENAI_API_KEY=sk-...` is in the file
- Restart the server after adding the key

### Still using Groq?
- Check logs for `using_groq` - this means OpenAI failed
- Verify your OpenAI API key is valid
- Check your OpenAI account has credits/quota

### Rate limit errors?
- OpenAI has rate limits based on your plan
- The system will log errors if rate limited
- Consider using `gpt-4o-mini` (cheaper, higher limits)

## Cost Notes

**OpenAI Pricing (as of Jan 2026):**
- `gpt-4o-mini`: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- `gpt-4o`: ~$2.50 per 1M input tokens, ~$10 per 1M output tokens

**Recommendation:** Use `gpt-4o-mini` for testing and production (it's very capable and much cheaper).
