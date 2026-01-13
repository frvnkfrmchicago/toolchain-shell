"""Supervisor agent - orchestrates the workflow by routing to specialists."""

import structlog
from langchain_core.prompts import ChatPromptTemplate

from src.agents.llm import get_llm
from src.agents.state import AgentState, RouterDecision
from src.metrics import track_query

log = structlog.get_logger()

SUPERVISOR_SYSTEM_PROMPT = """You are a supervisor managing a team of AI tool experts.
Your job is to analyze user queries and decide which specialist agent should handle them.

Available agents:
- SEARCH: Call when user asks about recent news, updates, or information not in our database
- RAG: Call when user asks about AI tools, comparisons, recommendations, or needs tool information
- EXPLAIN: Call after RAG/SEARCH to synthesize results into a helpful response
- FINISH: Call ONLY after EXPLAIN has generated a final_response

Decision guidelines:
1. For tool questions (what tool for X, compare A vs B) → start with RAG
2. For recent updates or news → start with SEARCH
3. After getting context from RAG or SEARCH → MUST call EXPLAIN
4. After EXPLAIN has synthesized a response → call FINISH
5. NEVER call FINISH unless final_response exists and is non-empty

Required flow:
- Iteration 0: Must call RAG or SEARCH
- After RAG/SEARCH: Must call EXPLAIN
- After EXPLAIN: Call FINISH

Current state:
- Query: {query}
- Retrieved context: {retrieved_context}
- Search results: {search_results}
- Final response exists: {has_final_response}
- Previous messages: {messages}
- Iteration: {iteration}

Based on the current state, decide which agent to call next."""


@track_query("supervisor")
async def supervisor(state: AgentState) -> AgentState:
    """Decide which agent to route to based on current state."""
    log.info("supervisor_start", query=state["query"], iteration=state["iteration"])
    
    # Prevent infinite loops
    if state["iteration"] >= 5:
        log.warning("supervisor_max_iterations", iteration=state["iteration"])
        return {
            "next_agent": "finish",
            "messages": ["Max iterations reached, finishing."],
        }
    
    # If we already have a final response, finish
    if state.get("final_response") and len(state["final_response"].strip()) > 0:
        return {"next_agent": "finish", "messages": []}

    # First iteration - MUST start with RAG or SEARCH
    if state["iteration"] == 0:
        # For tool questions, start with RAG
        # For news/recent queries, start with SEARCH
        # Default to RAG for most queries
        return {
            "next_agent": "rag",
            "messages": ["[Supervisor] Starting with RAG agent"],
            "iteration": state["iteration"] + 1,
        }
    
    # Create the LLM with structured output (OpenAI preferred, Groq fallback)
    llm = get_llm(
        model=None,  # Uses default based on provider
        temperature=0,
        structured_output=RouterDecision,
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SUPERVISOR_SYSTEM_PROMPT),
        ("human", "Decide the next agent to call."),
    ])
    
    chain = prompt | llm
    
    try:
        decision: RouterDecision = await chain.ainvoke({
            "query": state["query"],
            "retrieved_context": state.get("retrieved_context", "None"),
            "search_results": state.get("search_results", "None"),
            "has_final_response": bool(state.get("final_response")),
            "messages": "\n".join(state.get("messages", [])) or "None",
            "iteration": state["iteration"],
        })
        
        log.info(
            "supervisor_decision",
            next_agent=decision.next_agent,
            reasoning=decision.reasoning,
        )
        
        return {
            "next_agent": decision.next_agent,
            "messages": [f"[Supervisor] Routing to {decision.next_agent}: {decision.reasoning}"],
            "iteration": state["iteration"] + 1,
        }
        
    except Exception as e:
        log.error("supervisor_error", error=str(e))
        # Fallback to RAG for most queries
        return {
            "next_agent": "rag",
            "messages": ["[Supervisor] Defaulting to RAG for this query."],
            "iteration": state["iteration"] + 1,
        }
