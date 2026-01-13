"""Explain agent - synthesizes information into helpful responses."""

import structlog
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.agents.llm import get_llm
from src.agents.state import AgentState
from src.metrics import track_query

log = structlog.get_logger()

class ComparisonTable(BaseModel):
    """Structured table for comparison when explicitly requested."""

    columns: list[str] = Field(min_length=2)
    rows: list[list[str]] = Field(default_factory=list)


class AnswerOption(BaseModel):
    """Single tool option in the response."""

    name: str
    what_it_is: str
    best_for: str
    pricing: str | None = None
    notes: str | None = None


class StructuredAnswer(BaseModel):
    """Structured response that we format into markdown."""

    tldr: str | None = None
    recommendation: str
    why_this_fits: list[str]
    options: list[AnswerOption]
    tradeoffs: list[str]
    next_steps: list[str]
    comparison_table: ComparisonTable | None = None


class ConversationalAnswer(BaseModel):
    """Free-flowing conversational response for educational/definition queries."""

    content: str = Field(description="Natural prose explanation, written conversationally")


def _detect_query_type(query: str) -> str:
    """Detect query type: definition, comparison, or recommendation.
    
    - definition: Educational questions like "What is X?" -> conversational prose
    - comparison: "Compare X vs Y" -> structured with table
    - recommendation: "Best X for Y?" -> structured with options
    """
    lower = query.lower()
    
    # Definition/educational queries - respond conversationally
    if any(w in lower for w in ["what is", "what are", "explain", "how does", "how do", "why do", "why are", "define", "meaning of"]):
        return "definition"
    
    # Comparison queries - use table format
    if any(w in lower for w in ["compare", "vs", "versus", "difference between", "differences"]):
        return "comparison"
    
    # Default to recommendation for tool-selection queries
    return "recommendation"


CONVERSATIONAL_SYSTEM_PROMPT = """You are a friendly AI expert explaining developer tools and concepts.

Write a natural, conversational response that flows like you're explaining to a colleague. 
Do NOT use bullet points, numbered lists, or structured sections like "TL;DR" or "Options".
Write in clear, readable prose paragraphs.

Retrieved Context:
{retrieved_context}

Web Search Results:
{search_results}

User Query: {query}
"""


EXPLAIN_SYSTEM_PROMPT = """You are an AI tool expert helping developers choose the right tools.

Return a response as JSON that matches the provided schema exactly.

Rules:
- Do NOT include internal routing/tooling chatter (no "routing", "retrieving", "thinking").
- Only include "tldr" if the user explicitly asks for a TL;DR or summary.
- Only include "comparison_table" if the user explicitly asks for a table.
- Keep text concise and scannable.

Retrieved Context (from our database):
{retrieved_context}

Web Search Results (latest info):
{search_results}

User Query: {query}

Wants TL;DR: {wants_tldr}
Wants Table: {wants_table}
"""


def _wants_tldr(query: str) -> bool:
    lower = query.lower()
    return "tl;dr" in lower or "tldr" in lower or "summary" in lower


def _wants_table(query: str) -> bool:
    return "table" in query.lower()


def _format_table(table: ComparisonTable) -> str:
    columns = table.columns
    rows = table.rows

    if not columns or not rows:
        return ""

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body_lines = []
    for row in rows:
        padded = row + [""] * (len(columns) - len(row))
        body_lines.append("| " + " | ".join(padded[: len(columns)]) + " |")

    return "\n".join([header, separator, *body_lines])


def _format_markdown(answer: StructuredAnswer, wants_tldr: bool, wants_table: bool) -> str:
    parts: list[str] = []

    if wants_tldr and answer.tldr:
        parts.append("## TL;DR")
        parts.append(answer.tldr.strip())

    parts.append("## Recommendation")
    parts.append(answer.recommendation.strip())

    if answer.why_this_fits:
        parts.append("## Why This Fits")
        parts.extend([f"- {item.strip()}" for item in answer.why_this_fits if item.strip()])

    if answer.options:
        parts.append("## Options")
        for option in answer.options:
            parts.append(f"### {option.name.strip()}")
            parts.append(f"- What it is: {option.what_it_is.strip()}")
            parts.append(f"- Best for: {option.best_for.strip()}")
            if option.pricing:
                parts.append(f"- Pricing: {option.pricing.strip()}")
            if option.notes:
                parts.append(f"- Notes: {option.notes.strip()}")

    if wants_table and answer.comparison_table:
        table_markdown = _format_table(answer.comparison_table)
        if table_markdown:
            parts.append("## Comparison")
            parts.append(table_markdown)

    if answer.tradeoffs:
        parts.append("## Trade-offs")
        parts.extend([f"- {item.strip()}" for item in answer.tradeoffs if item.strip()])

    if answer.next_steps:
        parts.append("## Next Steps")
        parts.extend([f"- {item.strip()}" for item in answer.next_steps if item.strip()])

    return "\n\n".join(parts).strip()


@track_query("explain")
async def explain_agent(state: AgentState) -> AgentState:
    """Synthesize retrieved context into a helpful response."""
    log.info("explain_agent_start", query=state["query"])

    query = state["query"]
    query_type = _detect_query_type(query)
    wants_tldr = _wants_tldr(query)
    wants_table = _wants_table(query) or query_type == "comparison"
    
    log.info("explain_agent_routing", query_type=query_type)
    
    try:
        if query_type == "definition":
            # Use conversational mode for educational queries
            llm = get_llm(
                model=None,
                temperature=0.7,
                structured_output=ConversationalAnswer,
            )
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", CONVERSATIONAL_SYSTEM_PROMPT),
                ("human", "Please explain this clearly and conversationally."),
            ])
            
            chain = prompt | llm
            
            response: ConversationalAnswer = await chain.ainvoke({
                "query": query,
                "retrieved_context": state.get("retrieved_context", "No database results"),
                "search_results": state.get("search_results", "No web results"),
            })
            
            final_response = response.content.strip()
            
        else:
            # Use structured mode for recommendations and comparisons
            llm = get_llm(
                model=None,
                temperature=0.7,
                structured_output=StructuredAnswer,
            )
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", EXPLAIN_SYSTEM_PROMPT),
                ("human", "Please provide a comprehensive answer to the user's query."),
            ])
            
            chain = prompt | llm
            
            response: StructuredAnswer = await chain.ainvoke({
                "query": query,
                "retrieved_context": state.get("retrieved_context", "No database results"),
                "search_results": state.get("search_results", "No web results"),
                "wants_tldr": wants_tldr,
                "wants_table": wants_table,
            })
            
            final_response = _format_markdown(response, wants_tldr, wants_table)
        
        log.info("explain_agent_complete", response_length=len(final_response), query_type=query_type)
        
        return {
            "final_response": final_response,
            "messages": [f"[Explain] Generated {query_type} response"],
        }
        
    except Exception as e:
        log.error("explain_agent_error", error=str(e))
        return {
            "final_response": f"I encountered an error generating a response: {str(e)}",
            "messages": [f"[Explain] Error: {str(e)}"],
        }
