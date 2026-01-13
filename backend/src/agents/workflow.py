"""LangGraph workflow wiring all agents together."""

import structlog
from langgraph.graph import END, StateGraph

from src.agents.state import AgentState
from src.agents.supervisor import supervisor
from src.agents.search_agent import search_agent
from src.agents.rag_agent import rag_agent
from src.agents.explain_agent import explain_agent

log = structlog.get_logger()


def route_to_agent(state: AgentState) -> str:
    """Route to the next agent based on supervisor decision."""
    next_agent = state.get("next_agent") or "finish"

    if next_agent in {"search", "rag", "explain"}:
        return next_agent

    return "end"


def create_workflow() -> StateGraph:
    """Create and compile the LangGraph workflow."""
    
    # Create the graph with AgentState
    graph = StateGraph(AgentState)
    
    # Add nodes for each agent
    graph.add_node("supervisor", supervisor)
    graph.add_node("search", search_agent)
    graph.add_node("rag", rag_agent)
    graph.add_node("explain", explain_agent)
    
    # Set entry point
    graph.set_entry_point("supervisor")
    
    # Add conditional routing from supervisor
    graph.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "search": "search",
            "rag": "rag",
            "explain": "explain",
            "end": END,
        },
    )
    
    # All specialist agents return to supervisor
    graph.add_edge("search", "supervisor")
    graph.add_edge("rag", "supervisor")
    graph.add_edge("explain", "supervisor")
    
    return graph


# Compile the workflow
workflow = create_workflow().compile()


async def run_query(query: str) -> dict:
    """Run a query through the agent workflow."""
    log.info("workflow_start", query=query)
    
    initial_state: AgentState = {
        "query": query,
        "messages": [],
        "next_agent": None,
        "retrieved_context": "",
        "search_results": "",
        "final_response": "",
        "iteration": 0,
    }
    
    result = await workflow.ainvoke(initial_state)
    
    log.info("workflow_complete", final_response_length=len(result.get("final_response", "")))
    
    return result


async def stream_query(query: str, conversation_history: list[dict] | None = None):
    """Stream query results for real-time updates."""
    log.info("workflow_stream_start", query=query, has_history=bool(conversation_history))

    initial_state: AgentState = {
        "query": query,
        "messages": [],
        "next_agent": None,
        "retrieved_context": "",
        "search_results": "",
        "final_response": "",
        "iteration": 0,
        "conversation_history": conversation_history or [],
    }
    
    try:
        async for event in workflow.astream(initial_state):
            # Each event is a dict with the node name and its output
            for node_name, node_output in event.items():
                log.info("workflow_event", node=node_name, has_response=bool(node_output.get("final_response")))
                yield {
                    "node": node_name,
                    "messages": node_output.get("messages", []),
                    "final_response": node_output.get("final_response"),
                }
        
        log.info("workflow_stream_complete")
    except Exception as e:
        log.error("workflow_stream_error", error=str(e), exc_info=True)
        # Yield error so frontend can see it
        yield {
            "node": "error",
            "messages": [f"Workflow error: {str(e)}"],
            "final_response": f"I encountered an error processing your query: {str(e)}",
        }
        raise
