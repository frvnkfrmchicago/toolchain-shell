"""LLM provider helper - supports OpenAI (primary) and Groq (fallback)."""

import structlog
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel

from src.config import settings

log = structlog.get_logger()


def get_llm(
    model: str | None = None,
    temperature: float = 0.7,
    structured_output: type | None = None,
) -> BaseChatModel:
    """
    Get LLM instance with OpenAI as primary, Groq as fallback.
    
    Args:
        model: Model name (defaults based on provider)
        temperature: Sampling temperature
        structured_output: Pydantic model for structured output
        
    Returns:
        Configured LLM instance
    """
    # Try OpenAI first (if API key is set)
    if settings.openai_api_key:
        try:
            openai_model = model or "gpt-4o-mini"  # Fast, cheap default
            log.info("using_openai", model=openai_model)
            
            llm = ChatOpenAI(
                model=openai_model,
                temperature=temperature,
                api_key=settings.openai_api_key,
            )
            
            if structured_output:
                llm = llm.with_structured_output(structured_output)
            
            return llm
            
        except Exception as e:
            log.error("openai_init_failed", error=str(e), exc_info=True, falling_back="groq")
            # Don't fall through silently - log the error
    
    # Fallback to Groq
    if settings.groq_api_key:
        try:
            groq_model = model or "llama-3.3-70b-versatile"
            log.info("using_groq", model=groq_model)
            
            llm = ChatGroq(
                model=groq_model,
                temperature=temperature,
                api_key=settings.groq_api_key,
            )
            
            if structured_output:
                llm = llm.with_structured_output(structured_output)
            
            return llm
            
        except Exception as e:
            log.error("groq_init_failed", error=str(e))
    
    # No API keys available
    raise ValueError(
        "No LLM API key configured. Set OPENAI_API_KEY or GROQ_API_KEY in .env"
    )
