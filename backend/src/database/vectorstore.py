"""Chroma vector database setup and operations."""

from functools import lru_cache

import structlog
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import FakeEmbeddings

from src.cache import cached
from src.config import settings
from src.data.seed_tools import get_all_tools
from src.models.tool import AITool

log = structlog.get_logger()

_force_fake_embeddings = False

@lru_cache(maxsize=1)
def get_embeddings() -> OpenAIEmbeddings | FakeEmbeddings:
    """Get embeddings: OpenAI → Fake fallback (per ai-builder/rag/SKILL.md)."""
    
    # Try OpenAI (production quality)
    if not _force_fake_embeddings and settings.openai_api_key and "sk-" in settings.openai_api_key:
        try:
            embeddings_instance = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=settings.openai_api_key,
            )
            log.info("openai_embeddings_initialized", model="text-embedding-3-small")
            return embeddings_instance
        except Exception as e:
            log.error("openai_embeddings_init_failed", error=str(e), exc_info=True)
    
    if settings.allow_fake_embeddings:
        log.warning("using_fake_embeddings_not_production_ready")
        return FakeEmbeddings(size=1536)

    raise RuntimeError(
        "Embeddings are not configured. Set OPENAI_API_KEY or enable ALLOW_FAKE_EMBEDDINGS=true for dev."
    )


def validate_embeddings() -> None:
    """Validate embeddings configuration at startup."""
    global _force_fake_embeddings
    embeddings_instance = get_embeddings()

    if isinstance(embeddings_instance, OpenAIEmbeddings):
        try:
            embeddings_instance.embed_query("healthcheck")
            log.info("openai_embeddings_validated", model="text-embedding-3-small")
        except Exception as e:
            log.error("openai_embeddings_validation_failed", error=str(e))
            if settings.allow_fake_embeddings:
                _force_fake_embeddings = True
                get_embeddings.cache_clear()
                get_vectorstore.cache_clear()
                log.warning("falling_back_to_fake_embeddings")
                return

            raise RuntimeError(
                "Embeddings validation failed. Check OPENAI_API_KEY or set ALLOW_FAKE_EMBEDDINGS=true for dev."
            ) from e


@lru_cache(maxsize=1)
def get_vectorstore() -> Chroma:
    """Get or create the Chroma vector store."""
    embeddings_function = get_embeddings()
    try:
        vector_db = Chroma(
            persist_directory=settings.chroma_persist_path,
            embedding_function=embeddings_function,
            collection_name="tools"
        )
        log.info(f"ChromaDB initialized at {settings.chroma_persist_path} with collection 'tools'")
        return vector_db
    except Exception as e:
         log.error(f"Prior ChromaDB initialization failed: {e}")
         # Fallback to in-memory if disk fails
         vector_db = Chroma(
            embedding_function=embeddings_function,
            collection_name="tools"
        )
         log.warning("Falling back to ephemeral in-memory ChromaDB.")
         # Record fallback for observability
         from src.metrics import errors_total
         errors_total.labels(error_type="vectorstore_fallback", agent="vectorstore").inc()
         return vector_db


def tool_to_document(tool: AITool) -> Document:
    """Convert an AITool to a LangChain Document for indexing."""
    # Create rich text content for embedding
    content = f"""
{tool.name} - {tool.provider}
Category: {tool.category} / {tool.subcategory}
Pricing: {tool.pricing}
Languages: {', '.join(tool.languages)}

{tool.description}

Use cases: {', '.join(tool.use_cases)}

Pros:
{chr(10).join(f'- {p}' for p in tool.pros)}

Cons:
{chr(10).join(f'- {c}' for c in tool.cons)}

Alternatives: {', '.join(tool.alternatives)}
""".strip()

    return Document(
        page_content=content,
        metadata={
            "id": tool.id,
            "name": tool.name,
            "category": tool.category,
            "subcategory": tool.subcategory,
            "provider": tool.provider,
            "pricing": tool.pricing,
            "languages": ",".join(tool.languages),
            "popularity_score": tool.popularity_score,
            "documentation_url": tool.documentation_url,
        },
    )


def index_all_tools() -> int:
    """Index all seed tools into the vector store."""
    log.info("indexing_tools_start")
    
    vectorstore = get_vectorstore()
    tools = get_all_tools()
    
    # Convert tools to documents
    documents = [tool_to_document(tool) for tool in tools]
    ids = [tool.id for tool in tools]
    
    # Add to vector store
    vectorstore.add_documents(documents, ids=ids)
    
    log.info("indexing_tools_complete", count=len(tools))
    return len(tools)


@cached("tool_search", ttl=3600)
def search_tools(
    query: str,
    category: str | None = None,
    pricing: str | None = None,
    k: int = 5,
) -> list[dict]:
    """Search for tools by semantic similarity with optional filters."""
    vectorstore = get_vectorstore()
    
    # Build filter dict
    filter_dict = {}
    if category:
        filter_dict["category"] = category
    if pricing:
        filter_dict["pricing"] = pricing
    
    # Perform search
    results = vectorstore.similarity_search_with_score(
        query,
        k=k,
        filter=filter_dict if filter_dict else None,
    )
    
    # Format results
    formatted = []
    for doc, score in results:
        formatted.append({
            "id": doc.metadata.get("id"),
            "name": doc.metadata.get("name"),
            "category": doc.metadata.get("category"),
            "provider": doc.metadata.get("provider"),
            "pricing": doc.metadata.get("pricing"),
            "content": doc.page_content[:500],
            "similarity_score": 1 - score,  # Convert distance to similarity
        })
    
    return formatted


def get_retriever(k: int = 5):
    """Get a retriever for use in chains."""
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": k})


# Initialize on import if needed
def ensure_indexed():
    """Ensure the vector store is indexed."""
    validate_embeddings()
    vectorstore = get_vectorstore()
    collection = vectorstore._collection
    
    if collection.count() == 0:
        log.info("vectorstore_empty", action="indexing")
        index_all_tools()
    else:
        log.info("vectorstore_ready", count=collection.count())
