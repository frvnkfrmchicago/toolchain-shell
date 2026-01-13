"""Tests for the RAG agent."""

import pytest
from unittest.mock import patch

from src.agents.state import AgentState


class TestRAGAgent:
    """Test RAG agent context retrieval."""

    @pytest.mark.asyncio
    async def test_rag_agent_retrieves_context(self, sample_agent_state):
        """RAG agent should retrieve relevant context from vectorstore."""
        from src.agents.rag_agent import rag_agent
        
        with patch("src.agents.rag_agent.search_tools", return_value=[{"id": "openai-api"}]):
            result = await rag_agent(sample_agent_state)
            
            assert "retrieved_context" in result
            assert len(result["retrieved_context"]) > 0
            assert "messages" in result

    @pytest.mark.asyncio
    async def test_rag_agent_handles_empty_results(self, sample_agent_state):
        """RAG agent should handle empty search results gracefully."""
        from src.agents.rag_agent import rag_agent
        
        with patch("src.agents.rag_agent.search_tools", return_value=[]):
            result = await rag_agent(sample_agent_state)
            
            # Should still return a valid state
            assert "retrieved_context" in result
            assert "messages" in result

    @pytest.mark.asyncio
    async def test_rag_agent_adds_message(self, sample_agent_state):
        """RAG agent should add a message about its action."""
        from src.agents.rag_agent import rag_agent
        
        with patch("src.agents.rag_agent.search_tools", return_value=[{"id": "openai-api"}]):
            result = await rag_agent(sample_agent_state)
            
            assert len(result["messages"]) > 0
            assert "[RAG]" in result["messages"][0]
