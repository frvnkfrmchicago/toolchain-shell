"""Tests for the supervisor agent routing logic."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.agents.state import AgentState, RouterDecision


class TestSupervisorRouting:
    """Test supervisor agent routing decisions."""

    @pytest.mark.asyncio
    async def test_supervisor_routes_to_rag_for_tool_query(self, sample_agent_state):
        """Supervisor should route to RAG for tool-related queries."""
        from src.agents.supervisor import supervisor
        
        # Mock the LLM to return a decision
        mock_decision = RouterDecision(next_agent="rag", reasoning="Tool query detected")
        
        with patch("src.agents.supervisor.get_llm") as mock_get_llm, \
             patch("src.agents.supervisor.ChatPromptTemplate.from_messages") as mock_prompt_factory:
            mock_llm = MagicMock()
            mock_chain = MagicMock()
            mock_chain.ainvoke = AsyncMock(return_value=mock_decision)
            mock_prompt = MagicMock()
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)
            mock_get_llm.return_value = mock_llm
            mock_prompt_factory.return_value = mock_prompt
            
            result = await supervisor(sample_agent_state)
            
            assert result["next_agent"] == "rag"
            assert "messages" in result
            assert result["iteration"] == 1

    @pytest.mark.asyncio
    async def test_supervisor_finishes_when_max_iterations_reached(self):
        """Supervisor should finish when max iterations reached."""
        from src.agents.supervisor import supervisor
        
        state: AgentState = {
            "query": "test query",
            "messages": [],
            "next_agent": None,
            "retrieved_context": "",
            "search_results": "",
            "final_response": "",
            "iteration": 5,  # Max iterations
        }
        
        result = await supervisor(state)
        
        assert result["next_agent"] == "finish"
        assert "Max iterations" in result["messages"][0]

    @pytest.mark.asyncio
    async def test_supervisor_finishes_when_response_exists(self):
        """Supervisor should finish when final_response already exists."""
        from src.agents.supervisor import supervisor
        
        state: AgentState = {
            "query": "test query",
            "messages": [],
            "next_agent": None,
            "retrieved_context": "",
            "search_results": "",
            "final_response": "Already have a response",
            "iteration": 1,
        }
        
        result = await supervisor(state)
        
        assert result["next_agent"] == "finish"

    @pytest.mark.asyncio
    async def test_supervisor_falls_back_on_error(self, sample_agent_state):
        """Supervisor should fallback to RAG on LLM errors."""
        from src.agents.supervisor import supervisor
        
        with patch("src.agents.supervisor.get_llm") as mock_get_llm, \
             patch("src.agents.supervisor.ChatPromptTemplate.from_messages") as mock_prompt_factory:
            mock_llm = MagicMock()
            mock_chain = MagicMock()
            mock_chain.ainvoke = AsyncMock(side_effect=Exception("LLM error"))
            mock_prompt = MagicMock()
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)
            mock_get_llm.return_value = mock_llm
            mock_prompt_factory.return_value = mock_prompt
            
            result = await supervisor(sample_agent_state)
            
            assert result["next_agent"] == "rag"
            # Verify message is sanitized (no error details exposed)
            assert "defaulting to rag" in result["messages"][0].lower()
