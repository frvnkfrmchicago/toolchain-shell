"""Seed data for AI tools database - 50+ real tools with accurate metadata."""

from src.models.tool import AITool

SEED_TOOLS: list[AITool] = [
    # ============ APIs ============
    AITool(
        id="openai-api",
        name="OpenAI API",
        category="api",
        subcategory="llm",
        description="OpenAI API provides access to GPT-4, GPT-4o, embeddings, and DALL-E. Industry-leading language models for text generation, code completion, reasoning, and multimodal tasks. Supports function calling, JSON mode, and streaming responses.",
        provider="OpenAI",
        pricing="paid",
        languages=["Python", "JavaScript", "TypeScript", "Go", "Ruby", "C#"],
        use_cases=["Chatbots", "Content generation", "Code assistance", "Data extraction", "Embeddings"],
        documentation_url="https://platform.openai.com/docs",
        github_url="https://github.com/openai/openai-python",
        pypi_package="openai",
        npm_package="openai",
        code_example='''from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)''',
        pros=["Best-in-class models", "Excellent documentation", "Fast inference", "Strong function calling"],
        cons=["Expensive at scale", "Rate limits", "No self-hosting option"],
        alternatives=["Anthropic API", "Google Gemini API", "AWS Bedrock"],
        popularity_score=95,
    ),
    AITool(
        id="anthropic-api",
        name="Anthropic Claude API",
        category="api",
        subcategory="llm",
        description="Anthropic API provides access to Claude 3.5 Sonnet, Claude 3 Opus, and Claude 3 Haiku. Known for strong reasoning, long context windows (200K tokens), and Constitutional AI safety approach. Excellent for complex analysis and coding tasks.",
        provider="Anthropic",
        pricing="paid",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["Complex reasoning", "Long document analysis", "Code generation", "Research assistance"],
        documentation_url="https://docs.anthropic.com",
        github_url="https://github.com/anthropics/anthropic-sdk-python",
        pypi_package="anthropic",
        npm_package="@anthropic-ai/sdk",
        code_example='''import anthropic
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)
print(message.content[0].text)''',
        pros=["200K context window", "Strong reasoning", "Excellent code quality", "Safety-focused"],
        cons=["Smaller ecosystem", "No image generation", "Limited fine-tuning"],
        alternatives=["OpenAI API", "Google Gemini API", "Cohere"],
        popularity_score=90,
    ),
    AITool(
        id="google-gemini-api",
        name="Google Gemini API",
        category="api",
        subcategory="llm",
        description="Google Gemini API offers Gemini 3 Pro, Gemini 3 Flash, and multimodal capabilities. Native multimodal understanding (text, images, video, audio), strong reasoning, and integration with Google Cloud services.",
        provider="Google",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript", "Go", "Dart"],
        use_cases=["Multimodal analysis", "Code generation", "Image understanding", "Video analysis"],
        documentation_url="https://ai.google.dev/docs",
        github_url="https://github.com/google-gemini/generative-ai-python",
        pypi_package="google-generativeai",
        npm_package="@google/generative-ai",
        code_example='''import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-3-pro")
response = model.generate_content("Hello!")
print(response.text)''',
        pros=["Free tier available", "Native multimodal", "Long context (2M tokens)", "Fast inference"],
        cons=["Newer ecosystem", "Enterprise features behind paywall", "Regional availability"],
        alternatives=["OpenAI API", "Anthropic API", "AWS Bedrock"],
        popularity_score=85,
    ),
    AITool(
        id="tavily-api",
        name="Tavily API",
        category="api",
        subcategory="search",
        description="Tavily is a search API built specifically for AI agents. Returns clean, structured results optimized for LLM consumption. Includes answer extraction, topic filtering, and source citations.",
        provider="Tavily",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["AI agent web search", "Research automation", "Fact-checking", "News aggregation"],
        documentation_url="https://docs.tavily.com",
        github_url="https://github.com/tavily-ai/tavily-python",
        pypi_package="tavily-python",
        npm_package="@tavily/core",
        code_example='''from tavily import TavilyClient
client = TavilyClient(api_key="YOUR_API_KEY")
response = client.search("latest AI news", search_depth="advanced")
print(response["results"])''',
        pros=["Built for AI agents", "Clean structured output", "Fast responses", "Free tier (1000/month)"],
        cons=["Limited to web search", "No image search", "Newer service"],
        alternatives=["SerpAPI", "Serper", "Brave Search API"],
        popularity_score=75,
    ),
    AITool(
        id="serpapi",
        name="SerpAPI",
        category="api",
        subcategory="search",
        description="SerpAPI provides structured Google search results via API. Supports Google, Bing, YouTube, and 20+ search engines. Returns JSON with organic results, featured snippets, knowledge graphs, and more.",
        provider="SerpAPI",
        pricing="freemium",
        languages=["Python", "Ruby", "Node.js", "Java", "PHP", "Go"],
        use_cases=["SERP analysis", "Competitive research", "SEO monitoring", "Data extraction"],
        documentation_url="https://serpapi.com/search-api",
        github_url="https://github.com/serpapi/google-search-results-python",
        pypi_package="google-search-results",
        npm_package="serpapi",
        code_example='''from serpapi import GoogleSearch
search = GoogleSearch({"q": "AI tools", "api_key": "YOUR_KEY"})
results = search.get_dict()
print(results["organic_results"])''',
        pros=["Multiple search engines", "Rich structured data", "Reliable uptime", "Good documentation"],
        cons=["Expensive at scale", "100 free searches/month", "Rate limited"],
        alternatives=["Tavily API", "Serper", "Brave Search API"],
        popularity_score=70,
    ),
    AITool(
        id="cohere-api",
        name="Cohere API",
        category="api",
        subcategory="llm",
        description="Cohere provides Command models for generation and Embed models for embeddings. Strong enterprise focus with fine-tuning capabilities, RAG optimization, and multilingual support.",
        provider="Cohere",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript", "Go"],
        use_cases=["Enterprise AI", "Semantic search", "Text classification", "Multilingual NLP"],
        documentation_url="https://docs.cohere.com",
        github_url="https://github.com/cohere-ai/cohere-python",
        pypi_package="cohere",
        npm_package="cohere-ai",
        code_example='''import cohere
co = cohere.Client("YOUR_API_KEY")
response = co.chat(message="Hello!")
print(response.text)''',
        pros=["Enterprise-ready", "Fine-tuning support", "Strong embeddings", "Multilingual"],
        cons=["Smaller model selection", "Less community content", "Enterprise pricing"],
        alternatives=["OpenAI API", "Anthropic API", "Google Gemini API"],
        popularity_score=65,
    ),

    # ============ MCPs ============
    AITool(
        id="mcp-github",
        name="GitHub MCP",
        category="mcp",
        subcategory="developer-tools",
        description="Model Context Protocol server for GitHub integration. Allows AI agents to read repositories, search code, create issues, manage PRs, and access GitHub API functionality through a standardized interface.",
        provider="Anthropic/Community",
        pricing="free",
        languages=["TypeScript", "Python"],
        use_cases=["Code review automation", "Issue triage", "Repository analysis", "PR management"],
        documentation_url="https://modelcontextprotocol.io/servers/github",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-github",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "your-token" }
    }
  }
}''',
        pros=["Official MCP server", "Full GitHub API access", "Well-maintained", "Easy setup"],
        cons=["Requires token with permissions", "Rate limits apply", "Some features require Pro"],
        alternatives=["GitLab MCP", "Direct GitHub API"],
        popularity_score=85,
    ),
    AITool(
        id="mcp-postgres",
        name="PostgreSQL MCP",
        category="mcp",
        subcategory="database",
        description="Model Context Protocol server for PostgreSQL databases. Enables AI agents to query databases, inspect schemas, run analytics, and generate reports while maintaining security through connection pooling.",
        provider="Anthropic/Community",
        pricing="free",
        languages=["TypeScript", "Python"],
        use_cases=["Database querying", "Schema exploration", "Data analysis", "Report generation"],
        documentation_url="https://modelcontextprotocol.io/servers/postgres",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-postgres",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "postgresql://..." }
    }
  }
}''',
        pros=["Direct SQL access", "Schema introspection", "Read-only option", "Connection pooling"],
        cons=["Security considerations", "Complex query limits", "No write by default"],
        alternatives=["Supabase MCP", "MySQL MCP", "SQLite MCP"],
        popularity_score=80,
    ),
    AITool(
        id="mcp-filesystem",
        name="Filesystem MCP",
        category="mcp",
        subcategory="system",
        description="Model Context Protocol server for local filesystem access. Allows AI agents to read, write, and manage files within specified directories. Essential for code agents and file-based workflows.",
        provider="Anthropic",
        pricing="free",
        languages=["TypeScript", "Python"],
        use_cases=["File management", "Code editing", "Log analysis", "Config management"],
        documentation_url="https://modelcontextprotocol.io/servers/filesystem",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-filesystem",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}''',
        pros=["Essential for coding agents", "Sandboxed access", "Fast file operations", "Official support"],
        cons=["Security requires careful config", "Directory restrictions needed", "No remote filesystems"],
        alternatives=["Google Drive MCP", "S3 MCP"],
        popularity_score=90,
    ),
    AITool(
        id="mcp-slack",
        name="Slack MCP",
        category="mcp",
        subcategory="communication",
        description="Model Context Protocol server for Slack workspace integration. Enables AI agents to read messages, search conversations, post updates, and manage channels programmatically.",
        provider="Community",
        pricing="free",
        languages=["TypeScript", "Python"],
        use_cases=["Team communication", "Message search", "Automated updates", "Channel management"],
        documentation_url="https://modelcontextprotocol.io/servers/slack",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-slack",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": { "SLACK_BOT_TOKEN": "xoxb-..." }
    }
  }
}''',
        pros=["Full Slack API access", "Message history search", "Channel management", "Bot integration"],
        cons=["Requires bot token", "Workspace admin approval", "Rate limits"],
        alternatives=["Discord MCP", "Teams MCP"],
        popularity_score=70,
    ),
    AITool(
        id="mcp-playwright",
        name="Playwright MCP",
        category="mcp",
        subcategory="browser",
        description="Model Context Protocol server for browser automation using Playwright. Enables AI agents to navigate websites, interact with elements, take screenshots, and extract data from web pages.",
        provider="Community",
        pricing="free",
        languages=["TypeScript", "Python"],
        use_cases=["Web scraping", "UI testing", "Form automation", "Screenshot capture"],
        documentation_url="https://github.com/executeautomation/mcp-playwright",
        github_url="https://github.com/executeautomation/mcp-playwright",
        npm_package="@anthropic/mcp-playwright",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-playwright"]
    }
  }
}''',
        pros=["Full browser control", "Cross-browser support", "Screenshot/PDF", "Network interception"],
        cons=["Resource intensive", "Complex selectors", "Anti-bot detection"],
        alternatives=["Puppeteer MCP", "Selenium integration"],
        popularity_score=75,
    ),
    AITool(
        id="mcp-notion",
        name="Notion MCP",
        category="mcp",
        subcategory="productivity",
        description="Model Context Protocol server for Notion workspace integration. Allows AI agents to read pages, create content, search databases, and manage workspace organization.",
        provider="Community",
        pricing="free",
        languages=["TypeScript"],
        use_cases=["Knowledge management", "Documentation", "Project management", "Content creation"],
        documentation_url="https://github.com/modelcontextprotocol/servers",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-notion",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": { "NOTION_TOKEN": "secret_..." }
    }
  }
}''',
        pros=["Full Notion API access", "Database queries", "Page creation", "Search capability"],
        cons=["Requires integration setup", "API rate limits", "Complex permissions"],
        alternatives=["Obsidian MCP", "Confluence MCP"],
        popularity_score=72,
    ),

    # ============ SDKs ============
    AITool(
        id="langchain-sdk",
        name="LangChain",
        category="sdk",
        subcategory="agent-framework",
        description="LangChain is a Python and JavaScript framework for building LLM applications. Provides abstractions for chains, agents, memory, and tool use. Extensive integration ecosystem with 700+ components.",
        provider="LangChain",
        pricing="free",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["Chatbots", "RAG systems", "Agents", "Data processing pipelines"],
        documentation_url="https://python.langchain.com/docs",
        github_url="https://github.com/langchain-ai/langchain",
        pypi_package="langchain",
        npm_package="langchain",
        code_example='''from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])
chain = prompt | llm
response = chain.invoke({"input": "Hello!"})''',
        pros=["Huge ecosystem", "Active development", "Great documentation", "LangSmith integration"],
        cons=["Frequent breaking changes", "Can be over-abstracted", "Learning curve"],
        alternatives=["LlamaIndex", "Haystack", "Semantic Kernel"],
        popularity_score=92,
    ),
    AITool(
        id="llamaindex-sdk",
        name="LlamaIndex",
        category="sdk",
        subcategory="rag-framework",
        description="LlamaIndex is a data framework for LLM applications focused on RAG and data ingestion. Excellent for connecting custom data sources to LLMs with advanced indexing and retrieval strategies.",
        provider="LlamaIndex",
        pricing="free",
        languages=["Python", "TypeScript"],
        use_cases=["RAG systems", "Document Q&A", "Knowledge bases", "Data agents"],
        documentation_url="https://docs.llamaindex.ai",
        github_url="https://github.com/run-llama/llama_index",
        pypi_package="llama-index",
        npm_package="llamaindex",
        code_example='''from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What is this about?")''',
        pros=["RAG-optimized", "Many data connectors", "Advanced retrieval", "Good abstractions"],
        cons=["Narrower focus than LangChain", "Smaller community", "Python-first"],
        alternatives=["LangChain", "Haystack", "txtai"],
        popularity_score=80,
    ),
    AITool(
        id="vercel-ai-sdk",
        name="Vercel AI SDK",
        category="sdk",
        subcategory="web-framework",
        description="Vercel AI SDK is a TypeScript library for building AI-powered streaming UIs. First-class React/Next.js support with streaming, function calling, and provider-agnostic design.",
        provider="Vercel",
        pricing="free",
        languages=["TypeScript", "JavaScript"],
        use_cases=["Chat interfaces", "Streaming UIs", "AI web apps", "Next.js integration"],
        documentation_url="https://sdk.vercel.ai/docs",
        github_url="https://github.com/vercel/ai",
        npm_package="ai",
        code_example='''import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const { text } = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Hello!',
});''',
        pros=["Streaming-first", "React hooks", "Provider-agnostic", "Excellent DX"],
        cons=["TypeScript-only", "Web-focused", "Fewer integrations"],
        alternatives=["LangChain.js", "OpenAI SDK", "Anthropic SDK"],
        popularity_score=85,
    ),
    AITool(
        id="openai-sdk-python",
        name="OpenAI Python SDK",
        category="sdk",
        subcategory="llm-client",
        description="Official Python SDK for OpenAI API. Type-safe, async-ready client with streaming support, function calling, and full API coverage including GPT-4, embeddings, and DALL-E.",
        provider="OpenAI",
        pricing="free",
        languages=["Python"],
        use_cases=["API integration", "Chatbots", "Embeddings", "Image generation"],
        documentation_url="https://platform.openai.com/docs/libraries/python-library",
        github_url="https://github.com/openai/openai-python",
        pypi_package="openai",
        code_example='''from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True
)
for chunk in response:
    print(chunk.choices[0].delta.content, end="")''',
        pros=["Official SDK", "Type hints", "Async support", "Streaming"],
        cons=["OpenAI-only", "No offline mode", "API key required"],
        alternatives=["LangChain", "LiteLLM", "Anthropic SDK"],
        popularity_score=90,
    ),
    AITool(
        id="anthropic-sdk-python",
        name="Anthropic Python SDK",
        category="sdk",
        subcategory="llm-client",
        description="Official Python SDK for Anthropic Claude API. Provides type-safe access to Claude models with streaming, tool use, and message batching support.",
        provider="Anthropic",
        pricing="free",
        languages=["Python"],
        use_cases=["API integration", "Complex reasoning", "Tool use", "Long context"],
        documentation_url="https://docs.anthropic.com/en/api/client-sdks",
        github_url="https://github.com/anthropics/anthropic-sdk-python",
        pypi_package="anthropic",
        code_example='''import anthropic
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content[0].text)''',
        pros=["Official SDK", "Strong typing", "Tool use support", "Batch API"],
        cons=["Claude-only", "Smaller ecosystem", "Enterprise features limited"],
        alternatives=["OpenAI SDK", "LangChain", "LiteLLM"],
        popularity_score=82,
    ),

    # ============ CLIs ============
    AITool(
        id="claude-code-cli",
        name="Claude Code",
        category="cli",
        subcategory="coding-assistant",
        description="Claude Code is an agentic coding tool by Anthropic that runs in your terminal. Uses Claude as the AI backbone with MCP integration, codebase understanding, and autonomous coding capabilities.",
        provider="Anthropic",
        pricing="paid",
        languages=["Any"],
        use_cases=["Code generation", "Debugging", "Refactoring", "Codebase Q&A"],
        documentation_url="https://docs.anthropic.com/claude-code",
        github_url=None,
        npm_package="@anthropic-ai/claude-code",
        code_example='''# Install
npm install -g @anthropic-ai/claude-code

# Use in project
cd my-project
claude

# Ask Claude to help
> Add tests for the user service''',
        pros=["Terminal-native", "MCP support", "Codebase awareness", "Agentic capabilities"],
        cons=["Requires Claude subscription", "API costs", "Still evolving"],
        alternatives=["Cursor", "GitHub Copilot CLI", "Aider"],
        popularity_score=88,
    ),
    AITool(
        id="cursor-cli",
        name="Cursor",
        category="cli",
        subcategory="ide",
        description="Cursor is an AI-first code editor built on VS Code. Features inline AI editing, chat with codebase context, and multi-file changes. Supports Claude, GPT-4, and custom models.",
        provider="Cursor",
        pricing="freemium",
        languages=["Any"],
        use_cases=["Code editing", "AI pair programming", "Codebase exploration", "Refactoring"],
        documentation_url="https://docs.cursor.com",
        github_url=None,
        code_example='''# Install Cursor from cursor.com

# Use Cmd+K for inline edits
# Use Cmd+L for chat
# Use Cmd+I for composer (multi-file)

# Example inline prompt:
# "Add error handling and logging"''',
        pros=["VS Code compatible", "Excellent UX", "Multi-model support", "Free tier"],
        cons=["Closed source", "Subscription for pro", "Resource intensive"],
        alternatives=["Claude Code", "GitHub Copilot", "Windsurf"],
        popularity_score=92,
    ),
    AITool(
        id="github-copilot-cli",
        name="GitHub Copilot CLI",
        category="cli",
        subcategory="terminal-assistant",
        description="GitHub Copilot in the terminal. Explains commands, suggests fixes, and helps with shell operations. Natural language to CLI command translation.",
        provider="GitHub/Microsoft",
        pricing="paid",
        languages=["Bash", "Zsh", "PowerShell"],
        use_cases=["Command suggestions", "Shell scripting", "DevOps", "CLI learning"],
        documentation_url="https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line",
        github_url="https://github.com/github/gh-copilot",
        code_example='''# Install via GitHub CLI
gh extension install github/gh-copilot

# Ask for command
gh copilot suggest "find large files in this directory"

# Explain a command
gh copilot explain "tar -xvzf archive.tar.gz"''',
        pros=["Natural language to CLI", "Command explanations", "GitHub integration", "Safe suggestions"],
        cons=["Requires Copilot subscription", "Limited to CLI", "Sometimes verbose"],
        alternatives=["Claude Code", "Warp AI", "Fig"],
        popularity_score=75,
    ),
    AITool(
        id="aider-cli",
        name="Aider",
        category="cli",
        subcategory="coding-assistant",
        description="Aider is an open-source AI pair programming tool in the terminal. Works with GPT-4, Claude, and local models. Git-aware with automatic commits for changes.",
        provider="Paul Gauthier",
        pricing="free",
        languages=["Python", "JavaScript", "Any"],
        use_cases=["Pair programming", "Code refactoring", "Bug fixes", "Feature development"],
        documentation_url="https://aider.chat",
        github_url="https://github.com/paul-gauthier/aider",
        pypi_package="aider-chat",
        code_example='''# Install
pip install aider-chat

# Start with GPT-4
aider --model gpt-4

# Or with Claude
aider --model claude-3-5-sonnet

# In session: describe changes in natural language''',
        pros=["Open source", "Multi-model", "Git integration", "Auto-commits"],
        cons=["Terminal-only", "Learning curve", "API costs apply"],
        alternatives=["Claude Code", "Cursor", "GitHub Copilot"],
        popularity_score=78,
    ),

    # ============ Vector Databases ============
    AITool(
        id="pinecone-db",
        name="Pinecone",
        category="vector_db",
        subcategory="managed",
        description="Pinecone is a fully managed vector database for production AI applications. Offers serverless and pod-based deployments, metadata filtering, and enterprise security. Optimized for speed and scale.",
        provider="Pinecone",
        pricing="freemium",
        languages=["Python", "JavaScript", "Go", "Java"],
        use_cases=["Semantic search", "RAG", "Recommendation systems", "Anomaly detection"],
        documentation_url="https://docs.pinecone.io",
        github_url="https://github.com/pinecone-io/pinecone-python-client",
        pypi_package="pinecone",
        npm_package="@pinecone-database/pinecone",
        code_example='''from pinecone import Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index("my-index")

# Upsert vectors
index.upsert(vectors=[
    {"id": "doc1", "values": [0.1, 0.2, ...], "metadata": {"text": "..."}}
])

# Query
results = index.query(vector=[0.1, 0.2, ...], top_k=5)''',
        pros=["Fully managed", "Fast queries", "Metadata filtering", "Free tier"],
        cons=["Vendor lock-in", "Cost at scale", "No self-hosting"],
        alternatives=["Weaviate", "Qdrant", "Chroma", "pgvector"],
        popularity_score=88,
    ),
    AITool(
        id="chroma-db",
        name="Chroma",
        category="vector_db",
        subcategory="embedded",
        description="Chroma is an open-source embedding database for AI applications. Runs locally with zero configuration, perfect for development and prototyping. Supports persistence and multiple embedding functions.",
        provider="Chroma",
        pricing="free",
        languages=["Python", "JavaScript"],
        use_cases=["Local development", "Prototyping", "Small-scale RAG", "Testing"],
        documentation_url="https://docs.trychroma.com",
        github_url="https://github.com/chroma-core/chroma",
        pypi_package="chromadb",
        npm_package="chromadb",
        code_example='''import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./chroma_db")
ef = embedding_functions.OpenAIEmbeddingFunction(api_key="...")

collection = client.get_or_create_collection("tools", embedding_function=ef)
collection.add(documents=["AI tool description..."], ids=["tool-1"])

results = collection.query(query_texts=["vector database"], n_results=5)''',
        pros=["Zero config", "Local-first", "Python-native", "Fast iteration"],
        cons=["Not for production scale", "Limited distributed", "Newer project"],
        alternatives=["Pinecone", "Weaviate", "Qdrant", "LanceDB"],
        popularity_score=82,
    ),
    AITool(
        id="weaviate-db",
        name="Weaviate",
        category="vector_db",
        subcategory="hybrid",
        description="Weaviate is an open-source vector database with hybrid search (vector + keyword). Offers cloud and self-hosted options, GraphQL API, and built-in ML model integration.",
        provider="Weaviate",
        pricing="freemium",
        languages=["Python", "JavaScript", "Go", "Java"],
        use_cases=["Hybrid search", "RAG", "Multi-tenant apps", "Enterprise AI"],
        documentation_url="https://weaviate.io/developers/weaviate",
        github_url="https://github.com/weaviate/weaviate",
        pypi_package="weaviate-client",
        npm_package="weaviate-client",
        code_example='''import weaviate
from weaviate.classes.query import MetadataQuery

client = weaviate.connect_to_local()
collection = client.collections.get("Tools")

response = collection.query.hybrid(
    query="vector database for RAG",
    limit=5
)''',
        pros=["Hybrid search", "Self-hostable", "GraphQL API", "Multi-tenant"],
        cons=["More complex setup", "Resource intensive", "Learning curve"],
        alternatives=["Pinecone", "Qdrant", "Chroma", "Milvus"],
        popularity_score=78,
    ),
    AITool(
        id="qdrant-db",
        name="Qdrant",
        category="vector_db",
        subcategory="high-performance",
        description="Qdrant is a high-performance vector database written in Rust. Offers cloud and self-hosted options with advanced filtering, quantization, and horizontal scaling.",
        provider="Qdrant",
        pricing="freemium",
        languages=["Python", "JavaScript", "Rust", "Go"],
        use_cases=["High-performance search", "RAG", "Recommendation", "Similarity matching"],
        documentation_url="https://qdrant.tech/documentation",
        github_url="https://github.com/qdrant/qdrant",
        pypi_package="qdrant-client",
        npm_package="@qdrant/js-client-rest",
        code_example='''from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(":memory:")
client.create_collection("tools", vectors_config=VectorParams(size=1536, distance=Distance.COSINE))

client.upsert("tools", points=[
    {"id": 1, "vector": [...], "payload": {"name": "Tool 1"}}
])

results = client.search("tools", query_vector=[...], limit=5)''',
        pros=["Rust performance", "Advanced filtering", "Quantization", "Cloud + self-host"],
        cons=["Smaller community", "Fewer integrations", "Newer ecosystem"],
        alternatives=["Pinecone", "Weaviate", "Milvus", "Chroma"],
        popularity_score=76,
    ),
    AITool(
        id="pgvector-db",
        name="pgvector",
        category="vector_db",
        subcategory="postgres-extension",
        description="pgvector is a PostgreSQL extension for vector similarity search. Use your existing Postgres infrastructure for embeddings, combining relational and vector data in one database.",
        provider="pgvector Contributors",
        pricing="free",
        languages=["SQL", "Python", "JavaScript", "Any Postgres client"],
        use_cases=["Postgres-native apps", "Hybrid data", "Cost-effective RAG", "Existing infra"],
        documentation_url="https://github.com/pgvector/pgvector",
        github_url="https://github.com/pgvector/pgvector",
        code_example='''-- Enable extension
CREATE EXTENSION vector;

-- Create table with vector column
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding vector(1536)
);

-- Query with cosine similarity
SELECT * FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;''',
        pros=["Use existing Postgres", "ACID compliance", "Familiar SQL", "Cost-effective"],
        cons=["Performance limits at scale", "Manual optimization", "No managed option"],
        alternatives=["Pinecone", "Weaviate", "Supabase + pgvector"],
        popularity_score=80,
    ),
    AITool(
        id="milvus-db",
        name="Milvus",
        category="vector_db",
        subcategory="distributed",
        description="Milvus is a distributed vector database built for scale. Handles billions of vectors with GPU acceleration, multiple index types, and cloud-native architecture.",
        provider="Zilliz",
        pricing="freemium",
        languages=["Python", "Java", "Go", "Node.js"],
        use_cases=["Large-scale search", "Enterprise RAG", "Image search", "Recommendation"],
        documentation_url="https://milvus.io/docs",
        github_url="https://github.com/milvus-io/milvus",
        pypi_package="pymilvus",
        npm_package="@zilliz/milvus2-sdk-node",
        code_example='''from pymilvus import MilvusClient

client = MilvusClient("milvus_demo.db")
client.create_collection("tools", dimension=1536)

client.insert("tools", [
    {"id": 1, "vector": [...], "text": "Tool description"}
])

results = client.search("tools", data=[[...]], limit=5)''',
        pros=["Billion-scale", "GPU acceleration", "Multiple indexes", "Distributed"],
        cons=["Complex setup", "Resource heavy", "Overkill for small projects"],
        alternatives=["Pinecone", "Qdrant", "Weaviate"],
        popularity_score=74,
    ),

    # ============ Agent Frameworks ============
    AITool(
        id="langgraph-framework",
        name="LangGraph",
        category="agent_framework",
        subcategory="orchestration",
        description="LangGraph is a library for building stateful, multi-actor applications with LLMs. Uses graph-based workflows for complex agent orchestration with cycles, conditional logic, and persistence.",
        provider="LangChain",
        pricing="free",
        languages=["Python", "JavaScript"],
        use_cases=["Multi-agent systems", "Complex workflows", "Stateful agents", "Human-in-the-loop"],
        documentation_url="https://langchain-ai.github.io/langgraph/",
        github_url="https://github.com/langchain-ai/langgraph",
        pypi_package="langgraph",
        npm_package="@langchain/langgraph",
        code_example='''from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    messages: list

def agent(state: State) -> State:
    return {"messages": ["Agent response"]}

graph = StateGraph(State)
graph.add_node("agent", agent)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

app = graph.compile()
result = app.invoke({"messages": []})''',
        pros=["Graph-based control", "Cycles and loops", "Persistence", "LangChain integration"],
        cons=["LangChain dependency", "Learning curve", "Newer project"],
        alternatives=["AutoGen", "CrewAI", "Haystack"],
        popularity_score=85,
    ),
    AITool(
        id="autogen-framework",
        name="AutoGen",
        category="agent_framework",
        subcategory="multi-agent",
        description="AutoGen is Microsoft's framework for building multi-agent conversation systems. Supports complex agent interactions, code execution, and tool use with minimal configuration.",
        provider="Microsoft",
        pricing="free",
        languages=["Python"],
        use_cases=["Multi-agent chat", "Code generation", "Research automation", "Complex reasoning"],
        documentation_url="https://microsoft.github.io/autogen/",
        github_url="https://github.com/microsoft/autogen",
        pypi_package="autogen-agentchat",
        code_example='''from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent("assistant", llm_config={"model": "gpt-4"})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"use_docker": False})

user_proxy.initiate_chat(assistant, message="Write a Python fibonacci function")''',
        pros=["Easy multi-agent", "Code execution", "Microsoft backing", "Good defaults"],
        cons=["Less control than LangGraph", "OpenAI-focused", "Limited persistence"],
        alternatives=["LangGraph", "CrewAI", "Semantic Kernel"],
        popularity_score=80,
    ),
    AITool(
        id="crewai-framework",
        name="CrewAI",
        category="agent_framework",
        subcategory="role-based",
        description="CrewAI is a framework for orchestrating role-playing AI agents. Define crews with specific roles, goals, and tasks. Agents collaborate to complete complex objectives.",
        provider="CrewAI",
        pricing="free",
        languages=["Python"],
        use_cases=["Role-based agents", "Team simulation", "Research crews", "Content creation"],
        documentation_url="https://docs.crewai.com",
        github_url="https://github.com/crewAIInc/crewAI",
        pypi_package="crewai",
        code_example='''from crewai import Agent, Task, Crew

researcher = Agent(role="Researcher", goal="Find information", backstory="Expert researcher")
writer = Agent(role="Writer", goal="Write content", backstory="Technical writer")

task = Task(description="Research and write about AI tools", agent=researcher)
crew = Crew(agents=[researcher, writer], tasks=[task])

result = crew.kickoff()''',
        pros=["Intuitive role-based", "Easy to understand", "Good for teams", "Active community"],
        cons=["Less flexible than LangGraph", "Opinionated structure", "Newer project"],
        alternatives=["LangGraph", "AutoGen", "Haystack"],
        popularity_score=75,
    ),
    AITool(
        id="semantic-kernel",
        name="Semantic Kernel",
        category="agent_framework",
        subcategory="enterprise",
        description="Semantic Kernel is Microsoft's SDK for integrating LLMs into enterprise applications. Supports C#, Python, and Java with plugins, planners, and memory.",
        provider="Microsoft",
        pricing="free",
        languages=["Python", "C#", "Java"],
        use_cases=["Enterprise AI", ".NET integration", "Plugin systems", "Azure integration"],
        documentation_url="https://learn.microsoft.com/en-us/semantic-kernel/",
        github_url="https://github.com/microsoft/semantic-kernel",
        pypi_package="semantic-kernel",
        npm_package="semantic-kernel",
        code_example='''import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

kernel = sk.Kernel()
kernel.add_service(OpenAIChatCompletion(
    ai_model_id="gpt-4",
    api_key="..."
))

result = await kernel.invoke_prompt("Hello!")''',
        pros=["Enterprise-ready", ".NET first-class", "Azure integration", "Plugin architecture"],
        cons=["Microsoft-centric", "More verbose", "Smaller Python community"],
        alternatives=["LangChain", "LangGraph", "AutoGen"],
        popularity_score=70,
    ),
    AITool(
        id="haystack-framework",
        name="Haystack",
        category="agent_framework",
        subcategory="rag-pipeline",
        description="Haystack by deepset is an end-to-end NLP framework for building production RAG pipelines. Modular components for retrieval, generation, and evaluation.",
        provider="deepset",
        pricing="free",
        languages=["Python"],
        use_cases=["RAG pipelines", "Document search", "Question answering", "NLP workflows"],
        documentation_url="https://docs.haystack.deepset.ai",
        github_url="https://github.com/deepset-ai/haystack",
        pypi_package="haystack-ai",
        code_example='''from haystack import Pipeline
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator

pipeline = Pipeline()
pipeline.add_component("retriever", InMemoryBM25Retriever(document_store))
pipeline.add_component("generator", OpenAIGenerator(model="gpt-4"))
pipeline.connect("retriever", "generator")

result = pipeline.run({"retriever": {"query": "What is RAG?"}})''',
        pros=["Production-focused", "Modular design", "Evaluation tools", "Cloud offering"],
        cons=["Less agent-focused", "Smaller community", "Learning curve"],
        alternatives=["LangChain", "LlamaIndex", "txtai"],
        popularity_score=72,
    ),

    # ============ Additional APIs ============
    AITool(
        id="finnhub-api",
        name="Finnhub API",
        category="api",
        subcategory="financial-data",
        description="Finnhub provides real-time stock prices, company financials, news, and sentiment analysis. Free tier with WebSocket support for live data streaming.",
        provider="Finnhub",
        pricing="freemium",
        languages=["Python", "JavaScript", "Go", "Ruby"],
        use_cases=["Stock analysis", "Financial dashboards", "Trading bots", "News aggregation"],
        documentation_url="https://finnhub.io/docs/api",
        github_url="https://github.com/Finnhub-Stock-API/finnhub-python",
        pypi_package="finnhub-python",
        npm_package="finnhub",
        code_example='''import finnhub
client = finnhub.Client(api_key="YOUR_API_KEY")

# Get quote
quote = client.quote("AAPL")
print(f"Current price: {quote['c']}")

# Get company news
news = client.company_news("AAPL", _from="2024-01-01", to="2024-01-31")''',
        pros=["Free tier available", "Real-time WebSocket", "Comprehensive data", "Good documentation"],
        cons=["Rate limits on free", "US markets focus", "Premium for full data"],
        alternatives=["Alpha Vantage", "Polygon.io", "Yahoo Finance API"],
        popularity_score=68,
    ),
    AITool(
        id="telnyx-api",
        name="Telnyx API",
        category="api",
        subcategory="communications",
        description="Telnyx provides programmable SMS, voice, and fax APIs. Developer-friendly with WebSocket for real-time communication and global coverage.",
        provider="Telnyx",
        pricing="paid",
        languages=["Python", "JavaScript", "Ruby", "PHP", "Java"],
        use_cases=["SMS automation", "Voice calls", "IVR systems", "2FA"],
        documentation_url="https://developers.telnyx.com",
        github_url="https://github.com/team-telnyx/telnyx-python",
        pypi_package="telnyx",
        npm_package="telnyx",
        code_example='''import telnyx

telnyx.api_key = "YOUR_API_KEY"

message = telnyx.Message.create(
    from_="+15551234567",
    to="+15559876543",
    text="Hello from Telnyx!"
)''',
        pros=["Competitive pricing", "Global coverage", "Good developer experience", "WebSocket support"],
        cons=["Smaller than Twilio", "Setup complexity", "Number provisioning time"],
        alternatives=["Twilio", "Vonage", "MessageBird"],
        popularity_score=65,
    ),
    AITool(
        id="replicate-api",
        name="Replicate API",
        category="api",
        subcategory="ml-inference",
        description="Replicate runs open-source ML models in the cloud. Access Stable Diffusion, LLaMA, Whisper, and thousands of community models via simple API.",
        provider="Replicate",
        pricing="paid",
        languages=["Python", "JavaScript", "cURL"],
        use_cases=["Image generation", "Audio transcription", "Open-source LLMs", "Model experimentation"],
        documentation_url="https://replicate.com/docs",
        github_url="https://github.com/replicate/replicate-python",
        pypi_package="replicate",
        npm_package="replicate",
        code_example='''import replicate

output = replicate.run(
    "stability-ai/stable-diffusion:latest",
    input={"prompt": "astronaut riding a horse"}
)
print(output)''',
        pros=["Huge model selection", "No GPU needed", "Easy API", "Pay-per-use"],
        cons=["Cold starts", "Costs add up", "No fine-tuning"],
        alternatives=["HuggingFace Inference", "Modal", "Banana.dev"],
        popularity_score=75,
    ),
    AITool(
        id="huggingface-api",
        name="HuggingFace Inference API",
        category="api",
        subcategory="ml-inference",
        description="HuggingFace Inference API provides access to 200,000+ models for NLP, vision, audio, and multimodal tasks. Free tier available with serverless endpoints.",
        provider="HuggingFace",
        pricing="freemium",
        languages=["Python", "JavaScript", "cURL"],
        use_cases=["NLP tasks", "Embeddings", "Classification", "Summarization"],
        documentation_url="https://huggingface.co/docs/api-inference",
        github_url="https://github.com/huggingface/huggingface_hub",
        pypi_package="huggingface-hub",
        npm_package="@huggingface/inference",
        code_example='''from huggingface_hub import InferenceClient

client = InferenceClient()

# Text generation
result = client.text_generation(
    "The future of AI is",
    model="meta-llama/Llama-3.2-3B-Instruct"
)''',
        pros=["Huge model library", "Free tier", "Community models", "Open source"],
        cons=["Rate limits", "Variable quality", "Cold starts"],
        alternatives=["Replicate", "OpenAI", "Together AI"],
        popularity_score=85,
    ),

    # ============ NEW MCPs (Expansion) ============
    AITool(
        id="mcp-sqlite",
        name="SQLite MCP",
        category="mcp",
        subcategory="database",
        description="Model Context Protocol server for SQLite databases. Lightweight, file-based database access for AI agents. Perfect for local development, testing, and embedded applications.",
        provider="Anthropic/Community",
        pricing="free",
        languages=["TypeScript", "Python"],
        use_cases=["Local data storage", "Testing", "Embedded apps", "Prototyping"],
        documentation_url="https://modelcontextprotocol.io/servers/sqlite",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-sqlite",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/database.db"]
    }
  }
}''',
        pros=["Zero config", "File-based", "Fast queries", "Great for prototyping"],
        cons=["Not for production scale", "Single-file limitations", "No concurrent writes"],
        alternatives=["PostgreSQL MCP", "MySQL MCP", "DuckDB"],
        popularity_score=75,
    ),
    AITool(
        id="mcp-mysql",
        name="MySQL MCP",
        category="mcp",
        subcategory="database",
        description="Model Context Protocol server for MySQL and MariaDB databases. Enables AI agents to query relational data, inspect schemas, and run analytics on MySQL databases.",
        provider="Community",
        pricing="free",
        languages=["TypeScript", "Python"],
        use_cases=["Legacy database access", "E-commerce data", "WordPress integration", "MySQL analytics"],
        documentation_url="https://github.com/modelcontextprotocol/servers",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-mysql",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": { "MYSQL_URL": "mysql://user:pass@localhost/db" }
    }
  }
}''',
        pros=["Wide compatibility", "Schema introspection", "Read-only option", "Familiar SQL"],
        cons=["Security setup required", "Connection management", "No write by default"],
        alternatives=["PostgreSQL MCP", "SQLite MCP", "Supabase MCP"],
        popularity_score=72,
    ),
    AITool(
        id="mcp-mongodb",
        name="MongoDB MCP",
        category="mcp",
        subcategory="database",
        description="Model Context Protocol server for MongoDB databases. Enables AI agents to query document collections, aggregate data, and explore NoSQL schemas.",
        provider="Community",
        pricing="free",
        languages=["TypeScript", "Python"],
        use_cases=["Document queries", "NoSQL analytics", "Collection exploration", "Data aggregation"],
        documentation_url="https://github.com/modelcontextprotocol/servers",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-mongodb",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mongodb"],
      "env": { "MONGODB_URI": "mongodb://localhost:27017/mydb" }
    }
  }
}''',
        pros=["Document queries", "Aggregation pipelines", "Schema-free exploration", "Atlas support"],
        cons=["Complex queries limited", "Security considerations", "Read-focused"],
        alternatives=["PostgreSQL MCP", "Supabase MCP"],
        popularity_score=68,
    ),
    AITool(
        id="mcp-supabase",
        name="Supabase MCP",
        category="mcp",
        subcategory="database",
        description="Model Context Protocol server for Supabase. Access Postgres database, auth users, storage buckets, and edge functions through a unified interface.",
        provider="Community",
        pricing="free",
        languages=["TypeScript"],
        use_cases=["Full-stack apps", "User management", "File storage", "Realtime data"],
        documentation_url="https://github.com/supabase-community/supabase-mcp",
        github_url="https://github.com/supabase-community/supabase-mcp",
        npm_package="supabase-mcp",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "supabase-mcp"],
      "env": {
        "SUPABASE_URL": "https://xxx.supabase.co",
        "SUPABASE_KEY": "your-service-key"
      }
    }
  }
}''',
        pros=["All-in-one platform", "Auth + DB + Storage", "Postgres underneath", "Free tier"],
        cons=["Supabase-specific", "Service key required", "Community maintained"],
        alternatives=["PostgreSQL MCP", "Firebase MCP"],
        popularity_score=78,
    ),
    AITool(
        id="mcp-s3",
        name="AWS S3 MCP",
        category="mcp",
        subcategory="storage",
        description="Model Context Protocol server for Amazon S3. Enables AI agents to list buckets, read files, search objects, and manage cloud storage.",
        provider="Community",
        pricing="free",
        languages=["TypeScript", "Python"],
        use_cases=["File management", "Data lakes", "Backup access", "Asset management"],
        documentation_url="https://github.com/modelcontextprotocol/servers",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-s3",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "s3": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-s3"],
      "env": {
        "AWS_ACCESS_KEY_ID": "...",
        "AWS_SECRET_ACCESS_KEY": "...",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}''',
        pros=["Full S3 access", "Bucket browsing", "File content reading", "AWS native"],
        cons=["AWS credentials required", "Cost considerations", "No streaming for large files"],
        alternatives=["Google Drive MCP", "Dropbox MCP"],
        popularity_score=74,
    ),
    AITool(
        id="mcp-gdrive",
        name="Google Drive MCP",
        category="mcp",
        subcategory="storage",
        description="Model Context Protocol server for Google Drive. Search files, read documents, and manage folders in Google Workspace environments.",
        provider="Anthropic",
        pricing="free",
        languages=["TypeScript"],
        use_cases=["Document search", "File access", "Google Docs reading", "Workspace integration"],
        documentation_url="https://modelcontextprotocol.io/servers/google-drive",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-gdrive",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": { "GDRIVE_CREDENTIALS": "/path/to/credentials.json" }
    }
  }
}''',
        pros=["Official server", "Google Docs support", "Search capability", "Folder navigation"],
        cons=["OAuth setup required", "Rate limits", "Read-focused"],
        alternatives=["S3 MCP", "Dropbox MCP", "OneDrive MCP"],
        popularity_score=76,
    ),
    AITool(
        id="mcp-memory",
        name="Memory MCP",
        category="mcp",
        subcategory="ai-memory",
        description="Model Context Protocol server for persistent AI memory. Store and retrieve knowledge across conversations using a knowledge graph approach.",
        provider="Anthropic",
        pricing="free",
        languages=["TypeScript"],
        use_cases=["Persistent memory", "Knowledge graphs", "Context retention", "User preferences"],
        documentation_url="https://modelcontextprotocol.io/servers/memory",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-memory",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}''',
        pros=["Cross-conversation memory", "Knowledge graph", "No external DB needed", "Official support"],
        cons=["Local storage only", "Limited query capability", "Newer project"],
        alternatives=["Custom vector store", "Mem0"],
        popularity_score=82,
    ),
    AITool(
        id="mcp-brave-search",
        name="Brave Search MCP",
        category="mcp",
        subcategory="search",
        description="Model Context Protocol server for Brave Search. Privacy-focused web search for AI agents with clean, structured results.",
        provider="Anthropic",
        pricing="free",
        languages=["TypeScript"],
        use_cases=["Web search", "Research", "Fact-checking", "Privacy-focused search"],
        documentation_url="https://modelcontextprotocol.io/servers/brave-search",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-brave-search",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": { "BRAVE_API_KEY": "your-api-key" }
    }
  }
}''',
        pros=["Privacy-focused", "Clean results", "Official server", "Free tier"],
        cons=["API key required", "Less comprehensive than Google", "Newer API"],
        alternatives=["Tavily API", "SerpAPI", "Perplexity MCP"],
        popularity_score=70,
    ),
    AITool(
        id="mcp-linear",
        name="Linear MCP",
        category="mcp",
        subcategory="project-management",
        description="Model Context Protocol server for Linear. Manage issues, projects, and workflows. AI agents can create tickets, update status, and query project data.",
        provider="Community",
        pricing="free",
        languages=["TypeScript"],
        use_cases=["Issue tracking", "Sprint management", "Bug reporting", "Project queries"],
        documentation_url="https://github.com/jerhadf/linear-mcp",
        github_url="https://github.com/jerhadf/linear-mcp",
        npm_package="linear-mcp",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "linear-mcp"],
      "env": { "LINEAR_API_KEY": "lin_api_..." }
    }
  }
}''',
        pros=["Full Linear API access", "Issue creation", "Team queries", "Workflow automation"],
        cons=["Linear-specific", "API key required", "Community maintained"],
        alternatives=["Jira MCP", "GitHub Issues"],
        popularity_score=72,
    ),
    AITool(
        id="mcp-sentry",
        name="Sentry MCP",
        category="mcp",
        subcategory="monitoring",
        description="Model Context Protocol server for Sentry. Query error reports, analyze stack traces, and monitor application health through AI agents.",
        provider="Community",
        pricing="free",
        languages=["TypeScript", "Python"],
        use_cases=["Error analysis", "Bug triage", "Performance monitoring", "Alert management"],
        documentation_url="https://github.com/modelcontextprotocol/servers",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-sentry",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "sentry": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sentry"],
      "env": { "SENTRY_AUTH_TOKEN": "..." }
    }
  }
}''',
        pros=["Error investigation", "Stack trace analysis", "Issue grouping", "Release tracking"],
        cons=["Sentry subscription needed", "Read-focused", "Token permissions"],
        alternatives=["Datadog MCP", "Custom logging"],
        popularity_score=68,
    ),
    AITool(
        id="mcp-obsidian",
        name="Obsidian MCP",
        category="mcp",
        subcategory="knowledge",
        description="Model Context Protocol server for Obsidian vaults. Search notes, read markdown files, and navigate your personal knowledge base.",
        provider="Community",
        pricing="free",
        languages=["TypeScript"],
        use_cases=["Note search", "Knowledge retrieval", "Markdown access", "Second brain"],
        documentation_url="https://github.com/smithery-ai/mcp-obsidian",
        github_url="https://github.com/smithery-ai/mcp-obsidian",
        npm_package="mcp-obsidian",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian", "/path/to/vault"]
    }
  }
}''',
        pros=["Full vault access", "Markdown native", "Link navigation", "Search capability"],
        cons=["Local vaults only", "No sync support", "Community maintained"],
        alternatives=["Notion MCP", "Filesystem MCP"],
        popularity_score=74,
    ),
    AITool(
        id="mcp-puppeteer",
        name="Puppeteer MCP",
        category="mcp",
        subcategory="browser",
        description="Model Context Protocol server for Puppeteer browser automation. Navigate web pages, fill forms, and capture screenshots using Chrome.",
        provider="Anthropic",
        pricing="free",
        languages=["TypeScript"],
        use_cases=["Web scraping", "Form automation", "Screenshot capture", "Testing"],
        documentation_url="https://modelcontextprotocol.io/servers/puppeteer",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-puppeteer",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}''',
        pros=["Official server", "Full browser control", "Screenshot support", "DOM inspection"],
        cons=["Resource intensive", "Headless only", "Anti-bot detection"],
        alternatives=["Playwright MCP", "Selenium"],
        popularity_score=78,
    ),
    AITool(
        id="mcp-everart",
        name="EverArt MCP",
        category="mcp",
        subcategory="ai-image",
        description="Model Context Protocol server for AI image generation. Create images using various models through a standardized MCP interface.",
        provider="Community",
        pricing="free",
        languages=["TypeScript"],
        use_cases=["Image generation", "Art creation", "Design prototyping", "Visual content"],
        documentation_url="https://modelcontextprotocol.io/servers/everart",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-everart",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "everart": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everart"],
      "env": { "EVERART_API_KEY": "..." }
    }
  }
}''',
        pros=["Multiple models", "Easy generation", "MCP integrated", "Various styles"],
        cons=["API costs", "Quality varies", "Limited control"],
        alternatives=["DALL-E API", "Midjourney", "Stable Diffusion"],
        popularity_score=65,
    ),
    AITool(
        id="mcp-fetch",
        name="Fetch MCP",
        category="mcp",
        subcategory="web",
        description="Model Context Protocol server for fetching web content. Retrieve and parse web pages, APIs, and RSS feeds for AI consumption.",
        provider="Anthropic",
        pricing="free",
        languages=["TypeScript"],
        use_cases=["Web scraping", "API calls", "RSS reading", "Content extraction"],
        documentation_url="https://modelcontextprotocol.io/servers/fetch",
        github_url="https://github.com/modelcontextprotocol/servers",
        npm_package="@modelcontextprotocol/server-fetch",
        code_example='''// Configure in claude_desktop_config.json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}''',
        pros=["Simple HTTP requests", "Content parsing", "Official server", "No API key needed"],
        cons=["No JavaScript rendering", "Rate limiting needed", "Basic extraction"],
        alternatives=["Playwright MCP", "Puppeteer MCP"],
        popularity_score=80,
    ),

    # ============ NEW APIs (Expansion) ============
    AITool(
        id="mistral-api",
        name="Mistral API",
        category="api",
        subcategory="llm",
        description="Mistral AI provides open-weight and commercial LLMs. Mistral Large, Mistral Medium, and Mixtral models with strong performance and competitive pricing.",
        provider="Mistral AI",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["Text generation", "Code assistance", "Multilingual NLP", "Reasoning"],
        documentation_url="https://docs.mistral.ai",
        github_url="https://github.com/mistralai/client-python",
        pypi_package="mistralai",
        npm_package="@mistralai/mistralai",
        code_example='''from mistralai import Mistral

client = Mistral(api_key="YOUR_API_KEY")
response = client.chat.complete(
    model="mistral-large-latest",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)''',
        pros=["Open weights available", "Competitive pricing", "EU-based", "Strong multilingual"],
        cons=["Smaller ecosystem", "Fewer integrations", "Newer platform"],
        alternatives=["OpenAI API", "Anthropic API", "Together AI"],
        popularity_score=78,
    ),
    AITool(
        id="groq-api",
        name="Groq API",
        category="api",
        subcategory="llm",
        description="Groq provides ultra-fast LLM inference using custom LPU hardware. Access Llama, Mixtral, and Gemma models with industry-leading speed.",
        provider="Groq",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["Fast inference", "Real-time chat", "Voice AI", "Low-latency apps"],
        documentation_url="https://console.groq.com/docs",
        github_url="https://github.com/groq/groq-python",
        pypi_package="groq",
        npm_package="groq-sdk",
        code_example='''from groq import Groq

client = Groq()
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)''',
        pros=["10x faster inference", "Free tier", "Open model access", "Low latency"],
        cons=["Limited model selection", "Newer platform", "Rate limits"],
        alternatives=["OpenAI API", "Together AI", "Fireworks AI"],
        popularity_score=82,
    ),
    AITool(
        id="together-api",
        name="Together AI API",
        category="api",
        subcategory="llm",
        description="Together AI provides access to 200+ open-source models including Llama, Mistral, and custom fine-tuned models. Competitive pricing with fine-tuning support.",
        provider="Together AI",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["Open model access", "Fine-tuning", "Embeddings", "Batch inference"],
        documentation_url="https://docs.together.ai",
        github_url="https://github.com/togethercomputer/together-python",
        pypi_package="together",
        npm_package="together-ai",
        code_example='''from together import Together

client = Together()
response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)''',
        pros=["200+ models", "Fine-tuning", "Competitive pricing", "OpenAI-compatible"],
        cons=["Variable performance", "Model quality varies", "Newer platform"],
        alternatives=["Groq API", "Replicate", "Fireworks AI"],
        popularity_score=75,
    ),
    AITool(
        id="perplexity-api",
        name="Perplexity API",
        category="api",
        subcategory="search-llm",
        description="Perplexity provides LLMs with built-in web search. Get factual, cited answers with real-time information. Sonar models combine search and generation.",
        provider="Perplexity",
        pricing="paid",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["Research", "Fact-checking", "News analysis", "Real-time Q&A"],
        documentation_url="https://docs.perplexity.ai",
        github_url=None,
        pypi_package="openai",
        npm_package="openai",
        code_example='''from openai import OpenAI

client = OpenAI(
    api_key="YOUR_PPLX_KEY",
    base_url="https://api.perplexity.ai"
)
response = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "What happened today?"}]
)
print(response.choices[0].message.content)''',
        pros=["Built-in search", "Real-time info", "Citations included", "OpenAI-compatible"],
        cons=["No free tier", "Search-focused only", "Higher latency"],
        alternatives=["Tavily + GPT-4", "Google Gemini", "You.com API"],
        popularity_score=72,
    ),
    AITool(
        id="elevenlabs-api",
        name="ElevenLabs API",
        category="api",
        subcategory="audio",
        description="ElevenLabs provides AI voice synthesis with natural, human-like speech. Clone voices, generate speech, and create real-time voice applications.",
        provider="ElevenLabs",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["Text-to-speech", "Voice cloning", "Audiobooks", "Voice AI assistants"],
        documentation_url="https://elevenlabs.io/docs",
        github_url="https://github.com/elevenlabs/elevenlabs-python",
        pypi_package="elevenlabs",
        npm_package="elevenlabs",
        code_example='''from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")
audio = client.generate(
    text="Hello world!",
    voice="Rachel",
    model="eleven_multilingual_v2"
)
# audio is a generator of bytes''',
        pros=["Best-in-class quality", "Voice cloning", "Multilingual", "Low latency"],
        cons=["Expensive at scale", "Limited free tier", "Voice rights concerns"],
        alternatives=["OpenAI TTS", "Amazon Polly", "Google Cloud TTS"],
        popularity_score=85,
    ),
    AITool(
        id="deepgram-api",
        name="Deepgram API",
        category="api",
        subcategory="audio",
        description="Deepgram provides fast, accurate speech-to-text with real-time streaming. Supports 30+ languages with speaker diarization and transcription.",
        provider="Deepgram",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript", "Go"],
        use_cases=["Transcription", "Voice analytics", "Call center AI", "Meeting notes"],
        documentation_url="https://developers.deepgram.com",
        github_url="https://github.com/deepgram/deepgram-python-sdk",
        pypi_package="deepgram-sdk",
        npm_package="@deepgram/sdk",
        code_example='''from deepgram import DeepgramClient, PrerecordedOptions

client = DeepgramClient("YOUR_API_KEY")
options = PrerecordedOptions(model="nova-2", smart_format=True)

with open("audio.mp3", "rb") as f:
    response = client.listen.prerecorded.v("1").transcribe_file(
        {"buffer": f.read()}, options
    )
print(response.results.channels[0].alternatives[0].transcript)''',
        pros=["Fast real-time", "High accuracy", "Speaker diarization", "Competitive pricing"],
        cons=["Audio formats limited", "Latency on long files", "Learning curve"],
        alternatives=["Whisper API", "AssemblyAI", "AWS Transcribe"],
        popularity_score=78,
    ),
    AITool(
        id="assemblyai-api",
        name="AssemblyAI API",
        category="api",
        subcategory="audio",
        description="AssemblyAI provides speech-to-text, speaker diarization, and audio intelligence. LLM-powered features include summarization and sentiment analysis.",
        provider="AssemblyAI",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["Transcription", "Content moderation", "Summarization", "Audio analytics"],
        documentation_url="https://www.assemblyai.com/docs",
        github_url="https://github.com/AssemblyAI/assemblyai-python-sdk",
        pypi_package="assemblyai",
        npm_package="assemblyai",
        code_example='''import assemblyai as aai

aai.settings.api_key = "YOUR_API_KEY"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("audio.mp3")
print(transcript.text)''',
        pros=["LLM features built-in", "High accuracy", "Audio intelligence", "Easy SDK"],
        cons=["Processing time", "Premium features costly", "US-focused"],
        alternatives=["Deepgram", "Whisper API", "Rev.ai"],
        popularity_score=76,
    ),
    AITool(
        id="stability-api",
        name="Stability AI API",
        category="api",
        subcategory="image",
        description="Stability AI provides Stable Diffusion models via API. Generate, edit, and upscale images with industry-leading open-source image models.",
        provider="Stability AI",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["Image generation", "Image editing", "Upscaling", "Style transfer"],
        documentation_url="https://platform.stability.ai/docs",
        github_url="https://github.com/Stability-AI/stability-sdk",
        pypi_package="stability-sdk",
        npm_package="@stability-ai/rest",
        code_example='''import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from stability_sdk import client

stability_api = client.StabilityInference(key="YOUR_API_KEY")
answers = stability_api.generate(
    prompt="a beautiful sunset over mountains",
    engine="stable-diffusion-xl-1024-v1-0"
)''',
        pros=["Open model leadership", "Multiple models", "Image editing", "Competitive pricing"],
        cons=["Complex SDK", "Rate limits", "Quality varies by model"],
        alternatives=["DALL-E 3", "Midjourney", "Flux"],
        popularity_score=80,
    ),
    AITool(
        id="twilio-api",
        name="Twilio API",
        category="api",
        subcategory="communications",
        description="Twilio provides programmable SMS, voice, video, and email APIs. Industry standard for communication automation with global reach.",
        provider="Twilio",
        pricing="paid",
        languages=["Python", "JavaScript", "Ruby", "PHP", "Java", "C#", "Go"],
        use_cases=["SMS automation", "Voice calls", "2FA", "Video conferencing"],
        documentation_url="https://www.twilio.com/docs",
        github_url="https://github.com/twilio/twilio-python",
        pypi_package="twilio",
        npm_package="twilio",
        code_example='''from twilio.rest import Client

client = Client("ACCOUNT_SID", "AUTH_TOKEN")
message = client.messages.create(
    body="Hello from Twilio!",
    from_="+15551234567",
    to="+15559876543"
)
print(message.sid)''',
        pros=["Industry standard", "Global coverage", "Full-featured", "Great docs"],
        cons=["Expensive at scale", "Complex pricing", "Steep learning curve"],
        alternatives=["Telnyx", "Vonage", "MessageBird"],
        popularity_score=88,
    ),
    AITool(
        id="sendgrid-api",
        name="SendGrid API",
        category="api",
        subcategory="email",
        description="SendGrid provides email delivery and marketing APIs. Send transactional emails, manage campaigns, and track deliverability.",
        provider="Twilio/SendGrid",
        pricing="freemium",
        languages=["Python", "JavaScript", "Ruby", "PHP", "Java", "C#", "Go"],
        use_cases=["Transactional email", "Marketing campaigns", "Email analytics", "Templates"],
        documentation_url="https://docs.sendgrid.com",
        github_url="https://github.com/sendgrid/sendgrid-python",
        pypi_package="sendgrid",
        npm_package="@sendgrid/mail",
        code_example='''from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email="from@example.com",
    to_emails="to@example.com",
    subject="Hello",
    html_content="<p>Hello world!</p>"
)
sg = SendGridAPIClient("YOUR_API_KEY")
response = sg.send(message)''',
        pros=["High deliverability", "Free tier", "Great analytics", "Template editor"],
        cons=["Complex for simple use", "Pricing tiers confusing", "Twilio acquisition changes"],
        alternatives=["Resend", "Postmark", "Mailgun"],
        popularity_score=82,
    ),
    AITool(
        id="resend-api",
        name="Resend API",
        category="api",
        subcategory="email",
        description="Resend is a modern email API built for developers. Simple API, React Email support, and excellent developer experience.",
        provider="Resend",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript", "Go", "Ruby"],
        use_cases=["Transactional email", "React Email", "Developer tools", "SaaS products"],
        documentation_url="https://resend.com/docs",
        github_url="https://github.com/resend/resend-python",
        pypi_package="resend",
        npm_package="resend",
        code_example='''import resend

resend.api_key = "re_123456789"
email = resend.Emails.send({
    "from": "you@example.com",
    "to": "user@example.com",
    "subject": "Hello",
    "html": "<p>Hello world!</p>"
})''',
        pros=["Simple API", "React Email", "Modern DX", "Free tier"],
        cons=["Newer platform", "Fewer features than SendGrid", "Limited analytics"],
        alternatives=["SendGrid", "Postmark", "Mailgun"],
        popularity_score=75,
    ),
    AITool(
        id="voyage-api",
        name="Voyage AI API",
        category="api",
        subcategory="embeddings",
        description="Voyage AI provides state-of-the-art embedding models for RAG. Purpose-built for retrieval with domain-specific models for code, legal, and finance.",
        provider="Voyage AI",
        pricing="freemium",
        languages=["Python", "JavaScript"],
        use_cases=["RAG embeddings", "Code search", "Legal document search", "Semantic search"],
        documentation_url="https://docs.voyageai.com",
        github_url="https://github.com/voyage-ai/voyageai-python",
        pypi_package="voyageai",
        npm_package=None,
        code_example='''import voyageai

client = voyageai.Client(api_key="YOUR_API_KEY")
result = client.embed(
    ["Hello world", "Goodbye world"],
    model="voyage-3"
)
print(result.embeddings)''',
        pros=["Best-in-class retrieval", "Domain-specific models", "Optimized for RAG", "Reranking"],
        cons=["Embeddings only", "Newer platform", "Limited integrations"],
        alternatives=["OpenAI Embeddings", "Cohere Embed", "Jina Embeddings"],
        popularity_score=72,
    ),
    AITool(
        id="jina-api",
        name="Jina AI API",
        category="api",
        subcategory="embeddings",
        description="Jina AI provides embedding and reranking models. Multi-modal embeddings for text, images, and cross-modal search.",
        provider="Jina AI",
        pricing="freemium",
        languages=["Python", "JavaScript"],
        use_cases=["Multi-modal search", "Text embeddings", "Image embeddings", "Reranking"],
        documentation_url="https://jina.ai/embeddings",
        github_url="https://github.com/jina-ai/jina",
        pypi_package="jina",
        npm_package="@jina-ai/client",
        code_example='''import requests

response = requests.post(
    "https://api.jina.ai/v1/embeddings",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "input": ["Hello world"],
        "model": "jina-embeddings-v3"
    }
)
print(response.json()["data"][0]["embedding"])''',
        pros=["Multi-modal", "Long context", "Good quality", "Free tier"],
        cons=["Less popular than OpenAI", "Smaller ecosystem", "API only"],
        alternatives=["OpenAI Embeddings", "Voyage AI", "Cohere Embed"],
        popularity_score=70,
    ),
    AITool(
        id="stripe-api",
        name="Stripe API",
        category="api",
        subcategory="payments",
        description="Stripe provides payment processing APIs for online businesses. Accept payments, manage subscriptions, and handle payouts globally.",
        provider="Stripe",
        pricing="paid",
        languages=["Python", "JavaScript", "Ruby", "PHP", "Java", "C#", "Go"],
        use_cases=["Payment processing", "Subscriptions", "Invoicing", "Marketplace payments"],
        documentation_url="https://stripe.com/docs/api",
        github_url="https://github.com/stripe/stripe-python",
        pypi_package="stripe",
        npm_package="stripe",
        code_example='''import stripe

stripe.api_key = "sk_test_..."
payment_intent = stripe.PaymentIntent.create(
    amount=1000,
    currency="usd",
    payment_method_types=["card"],
)''',
        pros=["Industry standard", "Excellent docs", "Global coverage", "Strong security"],
        cons=["Per-transaction fees", "Complex for simple use", "Account holds possible"],
        alternatives=["Paddle", "LemonSqueezy", "PayPal"],
        popularity_score=95,
    ),
    AITool(
        id="alpha-vantage-api",
        name="Alpha Vantage API",
        category="api",
        subcategory="financial-data",
        description="Alpha Vantage provides free APIs for stock, forex, and crypto data. Historical and real-time data for financial analysis and trading.",
        provider="Alpha Vantage",
        pricing="freemium",
        languages=["Python", "JavaScript", "Any HTTP client"],
        use_cases=["Stock analysis", "Financial data", "Trading algorithms", "Market research"],
        documentation_url="https://www.alphavantage.co/documentation/",
        github_url=None,
        pypi_package="alpha-vantage",
        npm_package="alphavantage",
        code_example='''import requests

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "AAPL",
    "apikey": "YOUR_API_KEY"
}
response = requests.get("https://www.alphavantage.co/query", params=params)
data = response.json()''',
        pros=["Free tier generous", "Historical data", "Multiple asset classes", "Simple API"],
        cons=["Rate limits on free", "Data quality varies", "Delayed quotes"],
        alternatives=["Finnhub", "Polygon.io", "Yahoo Finance"],
        popularity_score=72,
    ),
    AITool(
        id="polygon-api",
        name="Polygon.io API",
        category="api",
        subcategory="financial-data",
        description="Polygon.io provides real-time and historical market data for stocks, options, forex, and crypto. Low-latency WebSocket feeds for trading.",
        provider="Polygon.io",
        pricing="freemium",
        languages=["Python", "JavaScript", "Go", "Rust"],
        use_cases=["Real-time quotes", "Options data", "Market analytics", "Algorithmic trading"],
        documentation_url="https://polygon.io/docs",
        github_url="https://github.com/polygon-io/client-python",
        pypi_package="polygon-api-client",
        npm_package="@polygon.io/client-js",
        code_example='''from polygon import RESTClient

client = RESTClient("YOUR_API_KEY")
aggs = client.get_aggs("AAPL", 1, "day", "2024-01-01", "2024-01-31")
for agg in aggs:
    print(agg)''',
        pros=["Real-time feeds", "High quality data", "Options + crypto", "Good free tier"],
        popularity_score=78,
    ),

    # ============ NEW SDKs (Expansion) ============
    AITool(
        id="litellm-sdk",
        name="LiteLLM",
        category="sdk",
        subcategory="llm-proxy",
        description="LiteLLM provides a unified interface for 100+ LLM providers. Call OpenAI, Anthropic, Cohere, Bedrock, and more with a single SDK. Great for multi-model strategies.",
        provider="BerriAI",
        pricing="free",
        languages=["Python"],
        use_cases=["Multi-model switching", "Cost optimization", "Fallback handling", "Load balancing"],
        documentation_url="https://docs.litellm.ai",
        github_url="https://github.com/BerriAI/litellm",
        pypi_package="litellm",
        code_example='''from litellm import completion

# Works with any model
response = completion(
    model="gpt-4o",  # or "claude-3-5-sonnet", "gemini/gemini-pro"
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)''',
        pros=["100+ providers", "Unified interface", "Cost tracking", "Fallback support"],
        cons=["Extra abstraction layer", "Version sync issues", "Debugging complexity"],
        alternatives=["OpenRouter", "Portkey", "LangChain"],
        popularity_score=82,
    ),
    AITool(
        id="instructor-sdk",
        name="Instructor",
        category="sdk",
        subcategory="structured-output",
        description="Instructor makes it easy to get structured outputs from LLMs. Built on Pydantic, works with OpenAI, Anthropic, and more. Essential for reliable data extraction.",
        provider="Jason Liu",
        pricing="free",
        languages=["Python"],
        use_cases=["Data extraction", "Structured outputs", "Validation", "Type-safe LLM calls"],
        documentation_url="https://python.useinstructor.com",
        github_url="https://github.com/jxnl/instructor",
        pypi_package="instructor",
        code_example='''import instructor
from pydantic import BaseModel
from openai import OpenAI

class User(BaseModel):
    name: str
    age: int

client = instructor.from_openai(OpenAI())
user = client.chat.completions.create(
    model="gpt-4o",
    response_model=User,
    messages=[{"role": "user", "content": "John is 30 years old"}]
)
print(user.name, user.age)''',
        pros=["Type-safe outputs", "Pydantic integration", "Retry logic", "Multi-provider"],
        cons=["Python-only", "Extra dependency", "Learning curve"],
        alternatives=["Outlines", "OpenAI function calling", "LangChain"],
        popularity_score=85,
    ),
    AITool(
        id="outlines-sdk",
        name="Outlines",
        category="sdk",
        subcategory="structured-output",
        description="Outlines provides structured generation for open-source LLMs. Guarantee valid JSON, regex patterns, or grammar-based outputs from local models.",
        provider="Outlines Dev",
        pricing="free",
        languages=["Python"],
        use_cases=["Local model structuring", "JSON generation", "Grammar constraints", "Regex matching"],
        documentation_url="https://outlines-dev.github.io/outlines/",
        github_url="https://github.com/outlines-dev/outlines",
        pypi_package="outlines",
        code_example='''import outlines

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, {"type": "object", "properties": {"name": {"type": "string"}}})

result = generator("Give me a person's name")
print(result)''',
        pros=["Guaranteed valid output", "Open-source models", "Grammar support", "Fast inference"],
        cons=["Local models focus", "Setup complexity", "Memory requirements"],
        alternatives=["Instructor", "Guidance", "LMQL"],
        popularity_score=72,
    ),
    AITool(
        id="dspy-sdk",
        name="DSPy",
        category="sdk",
        subcategory="prompt-optimization",
        description="DSPy is a framework for programming LLMs with composable modules. Automatically optimizes prompts and few-shot examples based on metrics.",
        provider="Stanford NLP",
        pricing="free",
        languages=["Python"],
        use_cases=["Prompt optimization", "Few-shot learning", "RAG pipelines", "Chain optimization"],
        documentation_url="https://dspy-docs.vercel.app",
        github_url="https://github.com/stanfordnlp/dspy",
        pypi_package="dspy-ai",
        code_example='''import dspy

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

class QA(dspy.Signature):
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()

qa = dspy.Predict(QA)
result = qa(question="What is the capital of France?")
print(result.answer)''',
        pros=["Auto-optimization", "Modular design", "Metric-driven", "Research-backed"],
        cons=["Steep learning curve", "Academic focus", "Different paradigm"],
        alternatives=["LangChain", "LlamaIndex", "Instructor"],
        popularity_score=75,
    ),
    AITool(
        id="supabase-js-sdk",
        name="Supabase JS",
        category="sdk",
        subcategory="baas",
        description="Supabase JavaScript SDK for database, auth, storage, and realtime. The open-source Firebase alternative with Postgres underneath.",
        provider="Supabase",
        pricing="freemium",
        languages=["JavaScript", "TypeScript"],
        use_cases=["Full-stack apps", "Auth", "Realtime subscriptions", "File storage"],
        documentation_url="https://supabase.com/docs/reference/javascript",
        github_url="https://github.com/supabase/supabase-js",
        npm_package="@supabase/supabase-js",
        code_example='''import { createClient } from '@supabase/supabase-js'

const supabase = createClient('https://xxx.supabase.co', 'anon-key')

// Query data
const { data } = await supabase.from('users').select('*')

// Auth
await supabase.auth.signInWithOAuth({ provider: 'github' })''',
        pros=["Open source", "Postgres power", "Great DX", "Generous free tier"],
        cons=["Postgres-specific", "Learning curve", "Self-host complexity"],
        alternatives=["Firebase", "Appwrite", "Nhost"],
        popularity_score=88,
    ),
    AITool(
        id="firebase-sdk",
        name="Firebase SDK",
        category="sdk",
        subcategory="baas",
        description="Firebase provides SDKs for web, iOS, and Android. Auth, Firestore, Realtime Database, Cloud Functions, and hosting in one platform.",
        provider="Google",
        pricing="freemium",
        languages=["JavaScript", "Python", "Swift", "Kotlin", "Flutter"],
        use_cases=["Mobile apps", "Web apps", "Auth", "Realtime sync"],
        documentation_url="https://firebase.google.com/docs",
        github_url="https://github.com/firebase/firebase-js-sdk",
        npm_package="firebase",
        pypi_package="firebase-admin",
        code_example='''import { initializeApp } from 'firebase/app'
import { getFirestore, collection, getDocs } from 'firebase/firestore'

const app = initializeApp({ /* config */ })
const db = getFirestore(app)

const snapshot = await getDocs(collection(db, 'users'))
snapshot.forEach((doc) => console.log(doc.data()))''',
        pros=["Google backing", "Mobile-first", "Great for prototyping", "Generous free tier"],
        cons=["Vendor lock-in", "Pricing complexity", "NoSQL limitations"],
        alternatives=["Supabase", "Appwrite", "AWS Amplify"],
        popularity_score=90,
    ),
    AITool(
        id="clerk-sdk",
        name="Clerk",
        category="sdk",
        subcategory="auth",
        description="Clerk provides drop-in authentication and user management. Pre-built UI components, social logins, MFA, and organization support.",
        provider="Clerk",
        pricing="freemium",
        languages=["JavaScript", "TypeScript", "React", "Next.js"],
        use_cases=["User auth", "Social login", "Organizations", "User management"],
        documentation_url="https://clerk.com/docs",
        github_url="https://github.com/clerk/javascript",
        npm_package="@clerk/nextjs",
        code_example='''// Next.js middleware
import { clerkMiddleware } from '@clerk/nextjs/server'
export default clerkMiddleware()

// Component
import { SignInButton, UserButton } from '@clerk/nextjs'

export function Header() {
  return <UserButton afterSignOutUrl="/" />
}''',
        pros=["Beautiful UI", "Easy setup", "Organizations", "Generous free tier"],
        cons=["Vendor lock-in", "Pricing at scale", "Next.js focused"],
        alternatives=["Auth0", "NextAuth", "Supabase Auth"],
        popularity_score=85,
    ),
    AITool(
        id="prisma-sdk",
        name="Prisma",
        category="sdk",
        subcategory="orm",
        description="Prisma is a next-generation Node.js ORM. Type-safe database client, migrations, and studio. Works with PostgreSQL, MySQL, SQLite, and more.",
        provider="Prisma",
        pricing="freemium",
        languages=["TypeScript", "JavaScript"],
        use_cases=["Database access", "Migrations", "Type-safe queries", "Schema management"],
        documentation_url="https://www.prisma.io/docs",
        github_url="https://github.com/prisma/prisma",
        npm_package="@prisma/client",
        code_example='''import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Type-safe queries
const users = await prisma.user.findMany({
  where: { email: { contains: '@example.com' } },
  include: { posts: true }
})''',
        pros=["Type safety", "Great DX", "Schema as code", "Visual studio"],
        cons=["Build step", "Performance overhead", "Learning curve"],
        alternatives=["Drizzle", "TypeORM", "Kysely"],
        popularity_score=90,
    ),
    AITool(
        id="drizzle-sdk",
        name="Drizzle ORM",
        category="sdk",
        subcategory="orm",
        description="Drizzle is a lightweight TypeScript ORM that feels like SQL. Zero dependencies, serverless-ready, with excellent type inference.",
        provider="Drizzle Team",
        pricing="free",
        languages=["TypeScript", "JavaScript"],
        use_cases=["Database access", "Serverless apps", "Edge functions", "Type-safe SQL"],
        documentation_url="https://orm.drizzle.team",
        github_url="https://github.com/drizzle-team/drizzle-orm",
        npm_package="drizzle-orm",
        code_example='''import { drizzle } from 'drizzle-orm/node-postgres'
import { users } from './schema'

const db = drizzle(process.env.DATABASE_URL)

const result = await db.select()
  .from(users)
  .where(eq(users.email, 'test@example.com'))''',
        pros=["SQL-like syntax", "Zero deps", "Edge-ready", "Fast"],
        cons=["Newer ecosystem", "Fewer resources", "Migration tooling"],
        alternatives=["Prisma", "Kysely", "TypeORM"],
        popularity_score=82,
    ),

    # ============ NEW CLIs (Expansion) ============
    AITool(
        id="ollama-cli",
        name="Ollama",
        category="cli",
        subcategory="local-llm",
        description="Ollama runs open-source LLMs locally. Download and run Llama, Mistral, Gemma, and more with a simple CLI. Great for development and privacy.",
        provider="Ollama",
        pricing="free",
        languages=["Any"],
        use_cases=["Local development", "Privacy-focused AI", "Model testing", "Offline inference"],
        documentation_url="https://ollama.com",
        github_url="https://github.com/ollama/ollama",
        code_example='''# Install
curl -fsSL https://ollama.com/install.sh | sh

# Run a model
ollama run llama3.2

# API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Hello!"
}' ''',
        pros=["Local inference", "Free", "Many models", "OpenAI-compatible API"],
        cons=["Requires GPU for speed", "Storage space", "No cloud option"],
        alternatives=["LM Studio", "llamafile", "vLLM"],
        popularity_score=92,
    ),
    AITool(
        id="modal-cli",
        name="Modal CLI",
        category="cli",
        subcategory="serverless-compute",
        description="Modal provides serverless Python infrastructure. Run GPU workloads, deploy functions, and scale ML models without managing infrastructure.",
        provider="Modal",
        pricing="freemium",
        languages=["Python"],
        use_cases=["GPU workloads", "ML deployment", "Batch processing", "Serverless functions"],
        documentation_url="https://modal.com/docs",
        github_url="https://github.com/modal-labs/modal-client",
        pypi_package="modal",
        code_example='''# Install
pip install modal

# Deploy a function
import modal

app = modal.App()

@app.function(gpu="T4")
def train_model():
    # Your GPU code here
    pass

# Run locally or deploy
modal run my_script.py''',
        pros=["Easy GPU access", "Pay-per-use", "Fast cold starts", "Great DX"],
        cons=["Python-only", "Vendor lock-in", "Debugging remote code"],
        alternatives=["Replicate", "RunPod", "Lambda Labs"],
        popularity_score=78,
    ),
    AITool(
        id="railway-cli",
        name="Railway CLI",
        category="cli",
        subcategory="deployment",
        description="Railway CLI deploys apps instantly. Push code, get a URL. Supports Node.js, Python, Go, Rust, and Docker with zero config.",
        provider="Railway",
        pricing="freemium",
        languages=["Any"],
        use_cases=["App deployment", "Database hosting", "CI/CD", "Preview environments"],
        documentation_url="https://docs.railway.app/reference/cli-api",
        github_url="https://github.com/railwayapp/cli",
        npm_package="@railway/cli",
        code_example='''# Install
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up

# Add Postgres
railway add -d postgres''',
        pros=["Zero config", "Fast deploys", "Built-in databases", "Great free tier"],
        cons=["Usage-based pricing", "Limited regions", "Smaller ecosystem"],
        alternatives=["Vercel", "Render", "Fly.io"],
        popularity_score=82,
    ),
    AITool(
        id="flyio-cli",
        name="Fly.io CLI",
        category="cli",
        subcategory="deployment",
        description="Fly.io CLI (flyctl) deploys apps to edge servers worldwide. Run containers close to users with built-in Postgres and Redis.",
        provider="Fly.io",
        pricing="freemium",
        languages=["Any"],
        use_cases=["Edge deployment", "Global apps", "Containers", "Databases"],
        documentation_url="https://fly.io/docs/flyctl/",
        github_url="https://github.com/superfly/flyctl",
        code_example='''# Install
curl -L https://fly.io/install.sh | sh

# Launch app
fly launch

# Deploy
fly deploy

# Add Postgres
fly postgres create''',
        pros=["Edge locations", "Container support", "Built-in databases", "Transparent pricing"],
        cons=["Learning curve", "Less integrated", "Debug complexity"],
        alternatives=["Railway", "Render", "AWS Lambda"],
        popularity_score=80,
    ),
    AITool(
        id="vercel-cli",
        name="Vercel CLI",
        category="cli",
        subcategory="deployment",
        description="Vercel CLI deploys frontend and serverless functions. Perfect for Next.js with preview deployments, edge functions, and instant rollbacks.",
        provider="Vercel",
        pricing="freemium",
        languages=["JavaScript", "TypeScript"],
        use_cases=["Frontend deployment", "Next.js", "Edge functions", "Preview URLs"],
        documentation_url="https://vercel.com/docs/cli",
        github_url="https://github.com/vercel/vercel",
        npm_package="vercel",
        code_example='''# Install
npm install -g vercel

# Deploy
vercel

# Production deploy
vercel --prod

# Set environment variables
vercel env add''',
        pros=["Best Next.js DX", "Instant deploys", "Preview URLs", "Edge network"],
        cons=["Frontend focused", "Pricing complexity", "Vendor lock-in"],
        alternatives=["Netlify", "Cloudflare Pages", "Railway"],
        popularity_score=92,
    ),
    AITool(
        id="cody-cli",
        name="Sourcegraph Cody",
        category="cli",
        subcategory="coding-assistant",
        description="Cody is an AI coding assistant with deep codebase understanding. Uses Sourcegraph's code graph for context-aware completions and explanations.",
        provider="Sourcegraph",
        pricing="freemium",
        languages=["Any"],
        use_cases=["Code understanding", "Codebase Q&A", "Code generation", "Refactoring"],
        documentation_url="https://docs.sourcegraph.com/cody",
        github_url="https://github.com/sourcegraph/cody",
        code_example='''# VS Code extension
# Install from marketplace

# CLI usage
cody chat "explain this function"
cody explain ./src/auth.ts

# Generate tests
cody generate tests ./src/utils.ts''',
        pros=["Deep context", "Open source", "Multiple IDEs", "Enterprise features"],
        cons=["Setup for codebase indexing", "Newer platform", "Resource intensive"],
        alternatives=["Claude Code", "Cursor", "GitHub Copilot"],
        popularity_score=75,
    ),
    AITool(
        id="continue-cli",
        name="Continue",
        category="cli",
        subcategory="coding-assistant",
        description="Continue is an open-source AI code assistant. Use any model (local or API) with VS Code or JetBrains. Fully customizable and privacy-focused.",
        provider="Continue",
        pricing="free",
        languages=["Any"],
        use_cases=["Code completion", "Chat with codebase", "Custom models", "Privacy"],
        documentation_url="https://docs.continue.dev",
        github_url="https://github.com/continuedev/continue",
        code_example='''// Install VS Code extension

// Configure in .continue/config.json
{
  "models": [
    {
      "title": "Ollama",
      "provider": "ollama",
      "model": "llama3.2"
    }
  ]
}

// Cmd+L to chat, Cmd+I for inline''',
        pros=["Open source", "Any model", "Privacy-focused", "Highly customizable"],
        cons=["Setup required", "Community support", "Less polished UX"],
        alternatives=["Cursor", "Claude Code", "Cody"],
        popularity_score=78,
    ),
    AITool(
        id="duckdb-cli",
        name="DuckDB CLI",
        category="cli",
        subcategory="database",
        description="DuckDB is an in-process SQL OLAP database. Analyze Parquet, CSV, and JSON directly. Fast analytics without infrastructure.",
        provider="DuckDB Foundation",
        pricing="free",
        languages=["Python", "Node.js", "R", "Julia", "Rust"],
        use_cases=["Data analysis", "Parquet queries", "Local analytics", "Data transformation"],
        documentation_url="https://duckdb.org/docs/",
        github_url="https://github.com/duckdb/duckdb",
        pypi_package="duckdb",
        npm_package="duckdb",
        code_example='''# CLI
duckdb

# Query Parquet directly
SELECT * FROM 'data.parquet' LIMIT 10;

# Query CSV
SELECT * FROM read_csv_auto('data.csv');

# Python
import duckdb
duckdb.sql("SELECT * FROM 'data.parquet'").show()''',
        pros=["No server needed", "Fast analytics", "Direct file access", "Embeddable"],
        cons=["OLAP focused", "Not for OLTP", "Memory limits"],
        alternatives=["SQLite", "ClickHouse", "Polars"],
        popularity_score=85,
    ),

    # ============ NEW Vector DBs (Expansion) ============
    AITool(
        id="lancedb-db",
        name="LanceDB",
        category="vector_db",
        subcategory="embedded",
        description="LanceDB is a serverless vector database built on Lance format. Embedded, with automatic versioning, and designed for AI/ML workloads.",
        provider="LanceDB",
        pricing="free",
        languages=["Python", "JavaScript", "Rust"],
        use_cases=["Local RAG", "ML pipelines", "Multi-modal search", "Data versioning"],
        documentation_url="https://lancedb.github.io/lancedb/",
        github_url="https://github.com/lancedb/lancedb",
        pypi_package="lancedb",
        npm_package="vectordb",
        code_example='''import lancedb

db = lancedb.connect("./my_db")
table = db.create_table("vectors", [
    {"id": 1, "vector": [0.1, 0.2, ...], "text": "hello"}
])

results = table.search([0.1, 0.2, ...]).limit(5).to_list()''',
        pros=["Serverless", "Versioning", "Multi-modal", "Lance format"],
        cons=["Newer project", "Smaller community", "Scaling limits"],
        alternatives=["Chroma", "Qdrant", "SQLite-VSS"],
        popularity_score=72,
    ),
    AITool(
        id="supabase-vector-db",
        name="Supabase pgvector",
        category="vector_db",
        subcategory="postgres",
        description="Supabase provides pgvector with managed Postgres. Vector search alongside your relational data with familiar SQL syntax.",
        provider="Supabase",
        pricing="freemium",
        languages=["SQL", "Python", "JavaScript"],
        use_cases=["RAG with relational data", "Hybrid queries", "Postgres apps", "Full-stack AI"],
        documentation_url="https://supabase.com/docs/guides/ai",
        github_url="https://github.com/supabase/supabase",
        code_example='''-- Enable extension
CREATE EXTENSION vector;

-- Create table
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding vector(1536)
);

-- Query
SELECT * FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;''',
        pros=["Managed Postgres", "SQL interface", "Hybrid data", "Great free tier"],
        cons=["Performance at scale", "Supabase dependency", "Index setup"],
        alternatives=["pgvector self-hosted", "Pinecone", "Weaviate"],
        popularity_score=82,
    ),
    AITool(
        id="turbopuffer-db",
        name="Turbopuffer",
        category="vector_db",
        subcategory="serverless",
        description="Turbopuffer is a serverless vector database built for speed. Extremely low latency with a focus on production workloads and cost efficiency.",
        provider="Turbopuffer",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["Low-latency search", "Production RAG", "Real-time recommendations", "Scale-to-zero"],
        documentation_url="https://turbopuffer.com/docs",
        github_url=None,
        pypi_package="turbopuffer",
        npm_package="turbopuffer",
        code_example='''import turbopuffer as tpuf

ns = tpuf.Namespace("my-namespace")
ns.upsert(
    ids=["1", "2"],
    vectors=[[0.1, 0.2, ...], [0.3, 0.4, ...]],
    attributes={"text": ["hello", "world"]}
)

results = ns.query(vector=[0.1, 0.2, ...], top_k=5)''',
        pros=["Ultra-low latency", "Serverless", "Cost-efficient", "Simple API"],
        cons=["Newer platform", "Limited features", "Smaller ecosystem"],
        alternatives=["Pinecone", "Qdrant", "Weaviate"],
        popularity_score=70,
    ),
    AITool(
        id="marqo-db",
        name="Marqo",
        category="vector_db",
        subcategory="multi-modal",
        description="Marqo is an end-to-end vector search engine. Built-in ML models for text and images, no separate embedding step needed.",
        provider="Marqo",
        pricing="freemium",
        languages=["Python"],
        use_cases=["Multi-modal search", "Image search", "Text search", "E-commerce"],
        documentation_url="https://docs.marqo.ai",
        github_url="https://github.com/marqo-ai/marqo",
        pypi_package="marqo",
        code_example='''import marqo

mq = marqo.Client(url="http://localhost:8882")
mq.create_index("my-index")

mq.index("my-index").add_documents([
    {"title": "AI Tools", "description": "Great for developers"},
    {"title": "ML Models", "image": "https://example.com/img.jpg"}
])

results = mq.index("my-index").search("developer tools")''',
        pros=["Built-in models", "Multi-modal", "No embedding step", "Self-hosted"],
        cons=["Resource intensive", "Smaller community", "Docker required"],
        alternatives=["Weaviate", "Qdrant", "Pinecone"],
        popularity_score=68,
    ),

    # ============ NEW Agent Frameworks (Expansion) ============
    AITool(
        id="openai-agents-sdk",
        name="OpenAI Agents SDK",
        category="agent_framework",
        subcategory="openai",
        description="OpenAI Agents SDK provides first-party agent building tools. Seamless integration with GPT-4, function calling, and the Assistants API.",
        provider="OpenAI",
        pricing="free",
        languages=["Python"],
        use_cases=["OpenAI agents", "Tool use", "Assistants", "Multi-turn conversations"],
        documentation_url="https://github.com/openai/openai-agents-python",
        github_url="https://github.com/openai/openai-agents-python",
        pypi_package="openai-agents",
        code_example='''from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    tools=[]
)

result = Runner.run_sync(agent, "Hello!")
print(result.final_output)''',
        pros=["OpenAI native", "Simple API", "First-party support", "Assistants integration"],
        cons=["OpenAI-only", "Newer SDK", "Less flexible"],
        alternatives=["LangGraph", "CrewAI", "AutoGen"],
        popularity_score=80,
    ),
    AITool(
        id="phidata-framework",
        name="Phidata",
        category="agent_framework",
        subcategory="agent-builder",
        description="Phidata provides tools to build AI Assistants with memory, knowledge, and tools. Simple API for creating production-ready agents.",
        provider="Phidata",
        pricing="free",
        languages=["Python"],
        use_cases=["AI assistants", "RAG agents", "Tool-using agents", "Multi-modal agents"],
        documentation_url="https://docs.phidata.com",
        github_url="https://github.com/phidatahq/phidata",
        pypi_package="phidata",
        code_example='''from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo

assistant = Assistant(
    tools=[DuckDuckGo()],
    show_tool_calls=True
)

assistant.print_response("What's happening in AI today?")''',
        pros=["Simple API", "Built-in tools", "Memory support", "Production-ready"],
        cons=["Smaller community", "Newer framework", "Less flexible"],
        alternatives=["LangGraph", "CrewAI", "AutoGen"],
        popularity_score=72,
    ),
    AITool(
        id="swarm-framework",
        name="OpenAI Swarm",
        category="agent_framework",
        subcategory="multi-agent",
        description="Swarm is OpenAI's experimental multi-agent framework. Lightweight orchestration for agent handoffs and routines with minimal abstraction.",
        provider="OpenAI",
        pricing="free",
        languages=["Python"],
        use_cases=["Multi-agent systems", "Agent handoffs", "Routines", "Experimentation"],
        documentation_url="https://github.com/openai/swarm",
        github_url="https://github.com/openai/swarm",
        pypi_package="openai-swarm",
        code_example='''from swarm import Swarm, Agent

client = Swarm()

agent = Agent(
    name="Agent",
    instructions="You are a helpful agent.",
)

response = client.run(agent=agent, messages=[{"role": "user", "content": "Hello!"}])
print(response.messages[-1]["content"])''',
        pros=["OpenAI official", "Minimal abstraction", "Easy handoffs", "Experimental"],
        cons=["Experimental only", "Limited features", "Not for production"],
        alternatives=["LangGraph", "AutoGen", "CrewAI"],
        popularity_score=68,
    ),
    AITool(
        id="smolagents-framework",
        name="smolagents",
        category="agent_framework",
        subcategory="huggingface",
        description="smolagents is HuggingFace's lightweight agent library. Build agents with any LLM and tools using simple Python code. Code-based agent actions.",
        provider="HuggingFace",
        pricing="free",
        languages=["Python"],
        use_cases=["Code agents", "Tool use", "Any LLM", "HuggingFace integration"],
        documentation_url="https://huggingface.co/docs/smolagents",
        github_url="https://github.com/huggingface/smolagents",
        pypi_package="smolagents",
        code_example='''from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel()
)

agent.run("Search for recent AI news and summarize it")''',
        pros=["Code-based actions", "HF ecosystem", "Any model", "Lightweight"],
        cons=["Newer library", "Limited docs", "Less production-ready"],
        alternatives=["LangGraph", "LangChain Agents", "AutoGen"],
        popularity_score=70,
    ),
    AITool(
        id="agentops-framework",
        name="AgentOps",
        category="agent_framework",
        subcategory="observability",
        description="AgentOps provides observability for AI agents. Track sessions, costs, errors, and performance across LangChain, CrewAI, AutoGen, and more.",
        provider="AgentOps",
        pricing="freemium",
        languages=["Python"],
        use_cases=["Agent monitoring", "Cost tracking", "Error analysis", "Performance optimization"],
        documentation_url="https://docs.agentops.ai",
        github_url="https://github.com/AgentOps-AI/agentops",
        pypi_package="agentops",
        code_example='''import agentops
agentops.init(api_key="YOUR_API_KEY")

# Works automatically with supported frameworks
from crewai import Agent, Task, Crew

# Your agent code here
# AgentOps tracks everything automatically

agentops.end_session("Success")''',
        pros=["Multi-framework", "Cost tracking", "Easy setup", "Free tier"],
        cons=["Observability only", "SDK integration", "Newer platform"],
        alternatives=["LangSmith", "Langfuse", "Helicone"],
        popularity_score=72,
    ),
    AITool(
        id="langfuse-framework",
        name="Langfuse",
        category="agent_framework",
        subcategory="observability",
        description="Langfuse is an open-source LLM engineering platform. Traces, evals, prompt management, and metrics for LLM applications.",
        provider="Langfuse",
        pricing="freemium",
        languages=["Python", "JavaScript", "TypeScript"],
        use_cases=["LLM observability", "Prompt management", "Evals", "Cost tracking"],
        documentation_url="https://langfuse.com/docs",
        github_url="https://github.com/langfuse/langfuse",
        pypi_package="langfuse",
        npm_package="langfuse",
        code_example='''from langfuse import Langfuse

langfuse = Langfuse()

trace = langfuse.trace(name="my-agent")
span = trace.span(name="llm-call")

# Your LLM code
response = openai.chat.completions.create(...)

span.end(output=response)
langfuse.flush()''',
        pros=["Open source", "Self-hostable", "Multi-framework", "Prompt management"],
        cons=["Setup required", "Less polished than LangSmith", "Smaller community"],
        alternatives=["LangSmith", "AgentOps", "Helicone"],
        popularity_score=78,
    ),
]


def get_all_tools() -> list[AITool]:
    """Return all seed tools."""
    return SEED_TOOLS


def get_tool_by_id(tool_id: str) -> AITool | None:
    """Get a tool by its ID."""
    for tool in SEED_TOOLS:
        if tool.id == tool_id:
            return tool
    return None


def get_tools_by_category(category: str) -> list[AITool]:
    """Get all tools in a category."""
    return [t for t in SEED_TOOLS if t.category == category]


def get_categories_with_counts() -> dict[str, int]:
    """Get category names with tool counts."""
    counts: dict[str, int] = {}
    for tool in SEED_TOOLS:
        counts[tool.category] = counts.get(tool.category, 0) + 1
    return counts
