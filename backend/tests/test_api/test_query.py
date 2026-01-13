"""Tests for API endpoints."""

import pytest
from unittest.mock import patch, AsyncMock


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check_returns_status(self, client):
        """Health endpoint should return healthy status."""
        with patch("src.agents.llm.get_llm"):
            response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestToolsEndpoint:
    """Test tools listing endpoint."""

    def test_list_tools(self, client):
        """Should return list of tools."""
        response = client.get("/api/tools")
        
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert "total" in data
        assert isinstance(data["tools"], list)

    def test_list_tools_with_category_filter(self, client):
        """Should filter tools by category."""
        response = client.get("/api/tools?category=framework")
        
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        # All returned tools should have the framework category
        for tool in data["tools"]:
            assert tool["category"] == "framework"

    def test_list_tools_with_limit(self, client):
        """Should respect limit parameter."""
        response = client.get("/api/tools?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["tools"]) <= 5


class TestCategoriesEndpoint:
    """Test categories endpoint."""

    def test_list_categories(self, client):
        """Should return list of categories."""
        response = client.get("/api/categories")
        
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert isinstance(data["categories"], list)
        
        # Each category should have id, name, count
        for cat in data["categories"]:
            assert "id" in cat
            assert "name" in cat
            assert "count" in cat


class TestQueryEndpoint:
    """Test query endpoint."""

    def test_query_endpoint_returns_response(self, client):
        """Query endpoint should return a valid response."""
        mock_result = {
            "final_response": "Here are some AI tools for you.",
            "messages": ["[Supervisor] Routing to RAG"],
        }
        
        with patch("src.api.main.run_query", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result
            
            response = client.post(
                "/api/query",
                json={"query": "What are the best vector databases?"}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "messages" in data
        assert data["query"] == "What are the best vector databases?"


class TestSubscribeEndpoint:
    """Test email subscription endpoint."""

    def test_subscribe_success(self, client):
        """Subscribe endpoint should accept valid email."""
        response = client.post(
            "/api/subscribe",
            json={"email": "test@example.com"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_subscribe_invalid_email(self, client):
        """Subscribe endpoint should reject invalid email."""
        response = client.post(
            "/api/subscribe",
            json={"email": "not-an-email"}
        )
        
        # Should get validation error
        assert response.status_code == 422
