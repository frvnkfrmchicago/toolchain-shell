"""Shared state and types for the multi-agent workflow."""

from typing import Annotated, Literal
import operator

from pydantic import BaseModel, Field, field_validator
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """Shared state across all agents in the workflow."""

    # User's original query
    query: str

    # Accumulated messages/responses from agents
    messages: Annotated[list[str], operator.add]

    # Which agent to route to next
    next_agent: Literal["search", "rag", "explain", "finish"] | None

    # Context retrieved from RAG
    retrieved_context: str

    # Web search results
    search_results: str

    # Final synthesized response
    final_response: str

    # Iteration count (to prevent infinite loops)
    iteration: int

    # Conversation history from frontend
    conversation_history: list[dict]


class RouterDecision(BaseModel):
    """Structured output for supervisor routing decisions."""
    
    next_agent: Literal["search", "rag", "explain", "finish"] = Field(
        description="Which agent to call next based on the query"
    )
    reasoning: str = Field(
        description="Brief explanation of why this agent was chosen"
    )

    @field_validator("next_agent", mode="before")
    def lowercase_agent(cls, v):
        """Force lowercase agent name."""
        if isinstance(v, str):
            return v.lower()
        return v
