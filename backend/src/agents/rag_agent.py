"""RAG agent - retrieves relevant tools from the vector database."""

import structlog

from src.agents.state import AgentState
from src.database.vectorstore import search_tools
from src.data.seed_tools import get_tool_by_id
from src.metrics import track_query

log = structlog.get_logger()


@track_query("rag")
async def rag_agent(state: AgentState) -> AgentState:
    """Retrieve relevant AI tools from the vector database."""
    log.info("rag_agent_start", query=state["query"])
    
    try:
        # Search the vector store
        results = search_tools(
            query=state["query"],
            k=5,
        )
        
        if not results:
            log.info("rag_agent_no_results")
            return {
                "retrieved_context": "No relevant tools found in the database.",
                "messages": ["[RAG] No matching tools found"],
            }
        
        # Format detailed context for the explain agent
        context_parts = []
        
        for result in results:
            tool_id = result.get("id")
            tool = get_tool_by_id(tool_id)
            
            if tool:
                context_parts.append(f"""
## {tool.name}
**Provider:** {tool.provider}
**Category:** {tool.category} / {tool.subcategory}
**Pricing:** {tool.pricing}
**Languages:** {', '.join(tool.languages)}

{tool.description}

**Use Cases:** {', '.join(tool.use_cases)}

**Pros:**
{chr(10).join(f'- {p}' for p in tool.pros)}

**Cons:**
{chr(10).join(f'- {c}' for c in tool.cons)}

**Alternatives:** {', '.join(tool.alternatives)}

**Documentation:** {tool.documentation_url}

**Code Example:**
```
{tool.code_example}
```
---
""")
        
        formatted_context = "\n".join(context_parts)
        
        log.info("rag_agent_complete", result_count=len(results))
        
        return {
            "retrieved_context": formatted_context,
            "messages": [f"[RAG] Retrieved {len(results)} relevant tools"],
        }
        
    except Exception as e:
        log.error("rag_agent_error", error=str(e))
        return {
            "retrieved_context": f"RAG error: {str(e)}",
            "messages": [f"[RAG] Error: {str(e)}"],
        }
