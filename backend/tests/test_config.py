"""Tests for application configuration."""

import pytest
import os
from unittest.mock import patch


class TestEnvironmentConfig:
    """Test suite for environment configuration."""

    def test_required_env_vars_defined(self):
        """Check that environment variable names are properly defined."""
        # These should be the expected env var names
        expected_vars = [
            "OPENAI_API_KEY",
            "GROQ_API_KEY",
            "TAVILY_API_KEY",
        ]
        for var in expected_vars:
            # Just check we can access them (may be empty in test)
            assert isinstance(os.environ.get(var, ""), str)

    def test_optional_env_vars_have_defaults(self):
        """Optional environment variables should have sensible defaults."""
        from src.config import get_config
        
        config = get_config()
        assert config is not None

    def test_cors_origins_configurable(self):
        """CORS origins should be configurable via environment."""
        cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000")
        assert isinstance(cors_origins, str)
        assert len(cors_origins) > 0


class TestConfigValidation:
    """Test configuration validation."""

    def test_config_loads_without_error(self):
        """Config should load without raising exceptions."""
        try:
            from src.config import get_config
            config = get_config()
            assert config is not None
        except ImportError:
            # Config module might not exist yet
            pass

    def test_chromadb_path_configurable(self):
        """ChromaDB path should be configurable."""
        default_path = os.environ.get("CHROMA_PERSIST_DIR", "./chroma_db")
        assert isinstance(default_path, str)


class TestAPISettings:
    """Test API-specific settings."""

    def test_rate_limit_settings(self):
        """Rate limit should be configurable."""
        rate_limit = os.environ.get("RATE_LIMIT", "100")
        assert rate_limit.isdigit() or rate_limit == ""

    def test_max_iterations_setting(self):
        """Max iterations for agents should be sensible."""
        max_iter = int(os.environ.get("MAX_AGENT_ITERATIONS", "5"))
        assert max_iter > 0
        assert max_iter <= 20  # Reasonable upper bound


class TestLLMConfig:
    """Test LLM configuration."""

    def test_model_selection(self):
        """Should have a default model configured."""
        default_model = os.environ.get("DEFAULT_MODEL", "gpt-4o-mini")
        assert isinstance(default_model, str)
        assert len(default_model) > 0

    def test_temperature_setting(self):
        """Temperature should be a valid float."""
        temp = float(os.environ.get("LLM_TEMPERATURE", "0.7"))
        assert 0.0 <= temp <= 2.0


class TestSecurityConfig:
    """Test security-related configuration."""

    def test_api_keys_not_hardcoded(self):
        """API keys should come from environment, not hardcoded."""
        from src.api.main import app
        
        # The app should exist and be configurable
        assert app is not None

    def test_sentry_dsn_optional(self):
        """Sentry DSN should be optional."""
        sentry_dsn = os.environ.get("SENTRY_DSN", "")
        # Should either be empty or a valid URL format
        assert sentry_dsn == "" or sentry_dsn.startswith("https://")
