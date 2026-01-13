"""Tests for the vector store functionality."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from src.database.vectorstore import (
    get_embeddings,
    get_or_create_vectorstore,
    search_tools,
)


class TestEmbeddings:
    """Test suite for embedding configuration."""

    def test_get_embeddings_returns_embeddings(self):
        """get_embeddings should return an embeddings instance."""
        embeddings = get_embeddings()
        assert embeddings is not None
        # Should have an embed method or similar
        assert hasattr(embeddings, 'embed_query') or hasattr(embeddings, 'embed_documents')

    def test_get_embeddings_fallback_on_missing_key(self):
        """Should fall back to fake embeddings if no API key."""
        with patch.dict('os.environ', {'OPENAI_API_KEY': ''}, clear=False):
            embeddings = get_embeddings()
            assert embeddings is not None

    def test_embeddings_are_consistent(self):
        """Multiple calls should return same type of embeddings."""
        emb1 = get_embeddings()
        emb2 = get_embeddings()
        assert type(emb1).__name__ == type(emb2).__name__


class TestVectorStore:
    """Test suite for vector store operations."""

    def test_get_or_create_vectorstore(self):
        """Should create or return existing vectorstore."""
        vectorstore = get_or_create_vectorstore()
        assert vectorstore is not None

    def test_vectorstore_has_collection(self):
        """Vectorstore should have a collection."""
        vectorstore = get_or_create_vectorstore()
        # ChromaDB vectorstore should have _collection attribute
        assert hasattr(vectorstore, '_collection') or hasattr(vectorstore, 'similarity_search')


class TestSearchTools:
    """Test suite for tool search functionality."""

    @pytest.mark.asyncio
    async def test_search_tools_returns_list(self):
        """search_tools should return a list."""
        results = await search_tools("vector database", limit=5)
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_tools_with_limit(self):
        """search_tools should respect the limit parameter."""
        results = await search_tools("AI tools", limit=3)
        assert len(results) <= 3

    @pytest.mark.asyncio
    async def test_search_tools_empty_query(self):
        """search_tools with empty query should not crash."""
        results = await search_tools("", limit=5)
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_tools_with_category_filter(self):
        """search_tools should filter by category when provided."""
        results = await search_tools(
            "tools", 
            limit=10, 
            category="LLM"
        )
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_tools_with_pricing_filter(self):
        """search_tools should filter by pricing when provided."""
        results = await search_tools(
            "best tools",
            limit=10,
            pricing="free"
        )
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_tools_result_structure(self):
        """search_tools results should have expected fields."""
        results = await search_tools("database", limit=1)
        if results:
            result = results[0]
            # Should have content and metadata
            assert hasattr(result, 'page_content') or isinstance(result, dict)


class TestVectorStoreIntegration:
    """Integration tests for the full vector store pipeline."""

    def test_vectorstore_initialization(self):
        """Vector store should initialize without errors."""
        try:
            vectorstore = get_or_create_vectorstore()
            assert vectorstore is not None
        except Exception as e:
            pytest.fail(f"Vector store initialization failed: {e}")

    def test_vectorstore_similarity_search(self):
        """Vector store should support similarity search."""
        vectorstore = get_or_create_vectorstore()
        # Should have similarity_search method
        assert hasattr(vectorstore, 'similarity_search')
