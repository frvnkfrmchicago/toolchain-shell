"""Search agent - performs web search for latest information."""

import structlog
from tavily import AsyncTavilyClient

from src.agents.state import AgentState
from src.config import settings
from src.metrics import track_query

log = structlog.get_logger()


@track_query("search")
async def search_agent(state: AgentState) -> AgentState:
    """Search the web for fresh information about AI tools."""
    log.info("search_agent_start", query=state["query"])
    
    if not settings.tavily_api_key:
        log.warning("search_agent_no_api_key")
        return {
            "search_results": "",
            "messages": ["[Search] Skipped - no Tavily API key"],
        }
    
    try:
        client = AsyncTavilyClient(api_key=settings.tavily_api_key)
        
        # Perform search with AI tool focus
        search_query = f"AI tools {state['query']}"
        
        response = await client.search(
            query=search_query,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
        )
        
        # Format results
        results = []
        
        # Include Tavily's AI-generated answer if available
        if response.get("answer"):
            results.append(f"Summary: {response['answer']}")
        
        # Include top search results
        for result in response.get("results", [])[:5]:
            results.append(
                f"- {result['title']}: {result['content'][:300]}..."
                f"\n  Source: {result['url']}"
            )
        
        formatted_results = "\n\n".join(results)
        
        log.info("search_agent_complete", result_count=len(response.get("results", [])))
        
        return {
            "search_results": formatted_results,
            "messages": [f"[Search] Found {len(response.get('results', []))} results"],
        }
        
    except Exception as e:
        log.error("search_agent_error", error=str(e))
        return {
            "search_results": f"Search error: {str(e)}",
            "messages": [f"[Search] Error: {str(e)}"],
        }
