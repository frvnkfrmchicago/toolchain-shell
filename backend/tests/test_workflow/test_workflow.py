"""End-to-end workflow tests."""

import pytest
from unittest.mock import patch, AsyncMock

from src.agents.state import AgentState


class TestWorkflowExecution:
    """Test full workflow execution."""

    @pytest.mark.asyncio
    async def test_workflow_completes_successfully(self, sample_agent_state):
        """Workflow should complete and return final response."""
        from src.agents.workflow import run_query
        
        mock_final_response = "Based on my analysis, Pinecone and Qdrant are excellent vector databases."
        
        with patch("src.agents.workflow.workflow.ainvoke", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {
                "final_response": mock_final_response,
                "messages": ["[Explain] Generated response"],
            }

            result = await run_query("What are the best vector databases?")

            assert result["final_response"] == mock_final_response

    @pytest.mark.asyncio
    async def test_workflow_handles_errors(self):
        """Workflow should handle errors gracefully."""
        from src.agents.workflow import run_query
        
        with patch("src.agents.workflow.workflow.ainvoke") as mock_invoke:
            mock_invoke.side_effect = Exception("Workflow error")
            
            with pytest.raises(Exception):
                await run_query("Test query")


class TestWorkflowRouting:
    """Test workflow routing logic."""

    def test_route_to_agent_returns_agent_name(self):
        """route_to_agent should return the correct agent name."""
        from src.agents.workflow import route_to_agent
        
        state: AgentState = {
            "query": "test",
            "messages": [],
            "next_agent": "rag",
            "retrieved_context": "",
            "search_results": "",
            "final_response": "",
            "iteration": 0,
        }
        
        result = route_to_agent(state)
        assert result == "rag"

    def test_route_to_agent_returns_end_for_finish(self):
        """route_to_agent should return 'end' when next_agent is 'finish'."""
        from src.agents.workflow import route_to_agent
        
        state: AgentState = {
            "query": "test",
            "messages": [],
            "next_agent": "finish",
            "retrieved_context": "",
            "search_results": "",
            "final_response": "",
            "iteration": 0,
        }
        
        result = route_to_agent(state)
        assert result == "end"

    def test_route_to_agent_defaults_to_end(self):
        """route_to_agent should default to 'end' when no next_agent."""
        from src.agents.workflow import route_to_agent
        
        state: AgentState = {
            "query": "test",
            "messages": [],
            "next_agent": None,
            "retrieved_context": "",
            "search_results": "",
            "final_response": "",
            "iteration": 0,
        }
        
        result = route_to_agent(state)
        assert result == "end"
