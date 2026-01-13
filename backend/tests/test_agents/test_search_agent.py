"""Tests for the search agent web search functionality."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.agents.state import AgentState


class TestSearchAgent:
    """Test search agent Tavily integration."""

    @pytest.fixture
    def search_state(self) -> AgentState:
        """State ready for web search."""
        return {
            "query": "Latest updates on LangChain v0.3",
            "messages": ["[Supervisor] Routing to search"],
            "next_agent": "search",
            "retrieved_context": "",
            "search_results": "",
            "final_response": "",
            "iteration": 1,
        }

    @pytest.mark.asyncio
    async def test_search_agent_returns_results(self, search_state):
        """Search agent should return formatted search results."""
        from src.agents.search_agent import search_agent

        mock_response = {
            "answer": "LangChain v0.3 includes improved agent capabilities.",
            "results": [
                {
                    "title": "LangChain v0.3 Release Notes",
                    "content": "Major updates include new agent framework...",
                    "url": "https://example.com/langchain"
                }
            ]
        }

        with patch("src.agents.search_agent.settings") as mock_settings, \
             patch("src.agents.search_agent.AsyncTavilyClient") as mock_client_class:
            mock_settings.tavily_api_key = "test-api-key"
            mock_client = MagicMock()
            mock_client.search = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            result = await search_agent(search_state)

            assert "search_results" in result
            assert len(result["search_results"]) > 0
            assert "messages" in result
            assert "[Search]" in result["messages"][0]

    @pytest.mark.asyncio
    async def test_search_agent_handles_no_api_key(self, search_state):
        """Search agent should gracefully skip when no API key configured."""
        from src.agents.search_agent import search_agent

        with patch("src.agents.search_agent.settings") as mock_settings:
            mock_settings.tavily_api_key = None

            result = await search_agent(search_state)

            assert "search_results" in result
            assert "unavailable" in result["search_results"].lower()
            assert "messages" in result
            assert "Skipped" in result["messages"][0] or "no" in result["messages"][0].lower()

    @pytest.mark.asyncio
    async def test_search_agent_handles_tavily_error(self, search_state):
        """Search agent should handle Tavily API errors gracefully."""
        from src.agents.search_agent import search_agent

        with patch("src.agents.search_agent.settings") as mock_settings, \
             patch("src.agents.search_agent.AsyncTavilyClient") as mock_client_class:
            mock_settings.tavily_api_key = "test-api-key"
            mock_client = MagicMock()
            mock_client.search = AsyncMock(side_effect=Exception("Tavily API error"))
            mock_client_class.return_value = mock_client

            result = await search_agent(search_state)

            # Should return error info, not crash
            assert "search_results" in result
            assert "error" in result["search_results"].lower()
            assert "messages" in result

    @pytest.mark.asyncio
    async def test_search_agent_formats_results_with_urls(self, search_state):
        """Search agent should include source URLs in formatted results."""
        from src.agents.search_agent import search_agent

        mock_response = {
            "results": [
                {
                    "title": "Test Result",
                    "content": "Test content here",
                    "url": "https://example.com/test"
                }
            ]
        }

        with patch("src.agents.search_agent.settings") as mock_settings, \
             patch("src.agents.search_agent.AsyncTavilyClient") as mock_client_class:
            mock_settings.tavily_api_key = "test-api-key"
            mock_client = MagicMock()
            mock_client.search = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            result = await search_agent(search_state)

            assert "https://example.com/test" in result["search_results"]
