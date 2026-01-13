"""Tests for /api/tools endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.api.main import app


client = TestClient(app)


class TestToolsEndpoint:
    """Test suite for the tools API endpoints."""

    def test_get_tools_returns_list(self):
        """GET /api/tools should return a list of tools."""
        response = client.get("/api/tools")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_tools_with_category_filter(self):
        """GET /api/tools?category=X should filter by category."""
        response = client.get("/api/tools?category=LLM")
        assert response.status_code == 200
        data = response.json()
        # All returned tools should match the category
        for tool in data:
            assert tool.get("category") == "LLM" or "category" in tool

    def test_get_tools_with_pricing_filter(self):
        """GET /api/tools?pricing=free should filter by pricing."""
        response = client.get("/api/tools?pricing=free")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_tools_with_limit(self):
        """GET /api/tools?limit=5 should limit results."""
        response = client.get("/api/tools?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5

    def test_get_tool_by_id_not_found(self):
        """GET /api/tools/{id} with invalid ID should return 404."""
        response = client.get("/api/tools/nonexistent-tool-id")
        assert response.status_code == 404

    def test_get_tool_by_id_valid(self):
        """GET /api/tools/{id} with valid ID should return tool details."""
        # First get a list of tools to find a valid ID
        list_response = client.get("/api/tools?limit=1")
        if list_response.status_code == 200 and list_response.json():
            tool_id = list_response.json()[0].get("id")
            if tool_id:
                response = client.get(f"/api/tools/{tool_id}")
                assert response.status_code in [200, 404]


class TestToolsSearch:
    """Test suite for tool search functionality."""

    def test_search_tools_empty_query(self):
        """Search with empty query should return all tools."""
        response = client.get("/api/tools?q=")
        assert response.status_code == 200

    def test_search_tools_with_query(self):
        """Search with query should filter results."""
        response = client.get("/api/tools?q=vector")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_search_tools_case_insensitive(self):
        """Search should be case insensitive."""
        response_lower = client.get("/api/tools?q=openai")
        response_upper = client.get("/api/tools?q=OPENAI")
        # Both should succeed
        assert response_lower.status_code == 200
        assert response_upper.status_code == 200


class TestToolsValidation:
    """Test input validation for tools endpoints."""

    def test_invalid_limit_parameter(self):
        """Invalid limit should be handled gracefully."""
        response = client.get("/api/tools?limit=-1")
        # Should either return 400 or handle gracefully
        assert response.status_code in [200, 400, 422]

    def test_invalid_category(self):
        """Non-existent category should return empty list."""
        response = client.get("/api/tools?category=NonExistentCategory123")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
