"""Pytest configuration and shared fixtures for ToolChain tests."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("ALLOW_FAKE_EMBEDDINGS", "true")

from src.api.main import app
from src.agents.state import AgentState


@pytest.fixture
def client():
    """FastAPI test client."""
    # Disable rate limiting for tests
    with patch("src.api.main.limiter.enabled", False):
        with TestClient(app) as c:
            yield c


@pytest.fixture
def async_client():
    """Async test client for async endpoints."""
    from httpx import AsyncClient, ASGITransport
    
    async def _get_client():
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            yield ac
    
    return _get_client


@pytest.fixture
def mock_llm():
    """Mock LLM that returns predictable responses."""
    mock = AsyncMock()
    mock.ainvoke = AsyncMock(return_value=MagicMock(
        content="This is a mock response about AI tools.",
        next_agent="rag",
        reasoning="User is asking about tools, routing to RAG."
    ))
    return mock


@pytest.fixture
def mock_vectorstore():
    """Mock vectorstore for RAG testing."""
    mock = MagicMock()
    mock.similarity_search = MagicMock(return_value=[
        MagicMock(
            page_content="LangChain is a framework for building LLM applications.",
            metadata={"name": "LangChain", "category": "framework"}
        ),
        MagicMock(
            page_content="Pinecone is a vector database for semantic search.",
            metadata={"name": "Pinecone", "category": "vector_db"}
        ),
    ])
    return mock


@pytest.fixture
def sample_agent_state() -> AgentState:
    """Sample agent state for testing workflows."""
    return {
        "query": "What are the best vector databases?",
        "messages": [],
        "next_agent": None,
        "retrieved_context": "",
        "search_results": "",
        "final_response": "",
        "iteration": 0,
    }


@pytest.fixture
def completed_agent_state() -> AgentState:
    """Agent state with completed response."""
    return {
        "query": "What are the best vector databases?",
        "messages": [
            "[Supervisor] Routing to rag: User asking about tools",
            "[RAG] Retrieved context about vector databases",
            "[Explain] Synthesizing response",
        ],
        "next_agent": "finish",
        "retrieved_context": "Pinecone, Qdrant, and Chroma are popular vector databases.",
        "search_results": "",
        "final_response": "The best vector databases include Pinecone, Qdrant, and Chroma.",
        "iteration": 3,
    }
