"""Tests for the explain agent response generation."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.agents.state import AgentState


class TestExplainAgent:
    """Test explain agent response synthesis."""

    @pytest.fixture
    def explain_state(self) -> AgentState:
        """State with context ready for explanation."""
        return {
            "query": "What are the best vector databases?",
            "messages": ["[RAG] Retrieved context about vector databases"],
            "next_agent": "explain",
            "retrieved_context": "Pinecone, Qdrant, and Chroma are popular vector databases.",
            "search_results": "",
            "final_response": "",
            "iteration": 2,
        }

    @pytest.mark.asyncio
    async def test_explain_agent_generates_response(self, explain_state):
        """Explain agent should generate a final response from context."""
        from src.agents.explain_agent import explain_agent

        mock_response = MagicMock()
        mock_response.content = "Here are the best vector databases for your needs..."

        with patch("src.agents.explain_agent.get_llm") as mock_get_llm, \
             patch("src.agents.explain_agent.ChatPromptTemplate.from_messages") as mock_prompt_factory:
            mock_llm = MagicMock()
            mock_chain = MagicMock()
            mock_chain.ainvoke = AsyncMock(return_value=mock_response)
            mock_prompt = MagicMock()
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)
            mock_get_llm.return_value = mock_llm
            mock_prompt_factory.return_value = mock_prompt

            result = await explain_agent(explain_state)

            assert "final_response" in result
            assert len(result["final_response"]) > 0
            assert "messages" in result

    @pytest.mark.asyncio
    async def test_explain_agent_handles_llm_error(self, explain_state):
        """Explain agent should handle LLM errors gracefully."""
        from src.agents.explain_agent import explain_agent

        with patch("src.agents.explain_agent.get_llm") as mock_get_llm, \
             patch("src.agents.explain_agent.ChatPromptTemplate.from_messages") as mock_prompt_factory:
            mock_llm = MagicMock()
            mock_chain = MagicMock()
            mock_chain.ainvoke = AsyncMock(side_effect=Exception("LLM API error"))
            mock_prompt = MagicMock()
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)
            mock_get_llm.return_value = mock_llm
            mock_prompt_factory.return_value = mock_prompt

            result = await explain_agent(explain_state)

            # Should return an error response, not crash
            assert "final_response" in result
            assert "error" in result["final_response"].lower()
            assert "messages" in result

    @pytest.mark.asyncio
    async def test_explain_agent_adds_message(self, explain_state):
        """Explain agent should add a message about its action."""
        from src.agents.explain_agent import explain_agent

        mock_response = MagicMock()
        mock_response.content = "Generated response"

        with patch("src.agents.explain_agent.get_llm") as mock_get_llm, \
             patch("src.agents.explain_agent.ChatPromptTemplate.from_messages") as mock_prompt_factory:
            mock_llm = MagicMock()
            mock_chain = MagicMock()
            mock_chain.ainvoke = AsyncMock(return_value=mock_response)
            mock_prompt = MagicMock()
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)
            mock_get_llm.return_value = mock_llm
            mock_prompt_factory.return_value = mock_prompt

            result = await explain_agent(explain_state)

            assert len(result["messages"]) > 0
            assert "[Explain]" in result["messages"][0]


class TestQueryTypeDetection:
    """Test query type detection for response routing."""

    def test_detect_definition_what_is(self):
        """'What is' questions should be detected as definition."""
        from src.agents.explain_agent import _detect_query_type
        assert _detect_query_type("What is a vector database?") == "definition"
        assert _detect_query_type("what is an MCP server?") == "definition"

    def test_detect_definition_explain(self):
        """'Explain' questions should be detected as definition."""
        from src.agents.explain_agent import _detect_query_type
        assert _detect_query_type("Explain how RAG works") == "definition"

    def test_detect_definition_how_does(self):
        """'How does' questions should be detected as definition."""
        from src.agents.explain_agent import _detect_query_type
        assert _detect_query_type("How does LangGraph work?") == "definition"

    def test_detect_comparison_vs(self):
        """'vs' questions should be detected as comparison."""
        from src.agents.explain_agent import _detect_query_type
        assert _detect_query_type("Pinecone vs Weaviate") == "comparison"
        assert _detect_query_type("Compare Pinecone vs Weaviate") == "comparison"

    def test_detect_comparison_difference(self):
        """'difference' questions should be detected as comparison."""
        from src.agents.explain_agent import _detect_query_type
        assert _detect_query_type("What's the difference between Chroma and Qdrant?") == "comparison"

    def test_detect_recommendation_default(self):
        """Tool selection questions should be detected as recommendation."""
        from src.agents.explain_agent import _detect_query_type
        assert _detect_query_type("Best MCP server for PostgreSQL?") == "recommendation"
        assert _detect_query_type("Which vector database should I use for RAG?") == "recommendation"
