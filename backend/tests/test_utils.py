"""
Tests for utility functions.

This module tests the helper functions in src/utils.py
"""

import pytest
from src.utils import (
    slugify,
    truncate,
    safe_get,
    format_tool_summary,
    parse_query_intent,
    validate_tool_data,
)


class TestSlugify:
    """Test cases for slugify function."""

    def test_basic_slugify(self):
        """Basic text should be converted to slug."""
        assert slugify("Hello World") == "hello-world"

    def test_special_characters_removed(self):
        """Special characters should be removed."""
        assert slugify("Hello! World?") == "hello-world"

    def test_multiple_spaces(self):
        """Multiple spaces should become single hyphen."""
        assert slugify("Hello    World") == "hello-world"

    def test_leading_trailing_spaces(self):
        """Leading and trailing spaces should be trimmed."""
        assert slugify("  Hello World  ") == "hello-world"

    def test_unicode_characters(self):
        """Unicode characters should be handled."""
        result = slugify("Café au lait")
        assert isinstance(result, str)

    def test_empty_string(self):
        """Empty string should return empty."""
        assert slugify("") == ""

    def test_numbers_preserved(self):
        """Numbers should be preserved."""
        assert slugify("Model v2.0") == "model-v20"


class TestTruncate:
    """Test cases for truncate function."""

    def test_short_text_unchanged(self):
        """Text shorter than max should be unchanged."""
        assert truncate("Hello", 100) == "Hello"

    def test_long_text_truncated(self):
        """Long text should be truncated with suffix."""
        result = truncate("This is a very long sentence", 20)
        assert len(result) <= 20
        assert result.endswith("...")

    def test_custom_suffix(self):
        """Custom suffix should be used."""
        result = truncate("Hello World Test", 15, "…")
        assert result.endswith("…")

    def test_exact_length(self):
        """Text at exact length should be unchanged."""
        text = "Exact"
        assert truncate(text, 5) == text


class TestSafeGet:
    """Test cases for safe_get function."""

    def test_simple_key(self):
        """Simple key should return value."""
        data = {"name": "Test"}
        assert safe_get(data, "name") == "Test"

    def test_nested_key(self):
        """Nested key should return nested value."""
        data = {"user": {"profile": {"name": "John"}}}
        assert safe_get(data, "user.profile.name") == "John"

    def test_missing_key_returns_default(self):
        """Missing key should return default."""
        data = {"name": "Test"}
        assert safe_get(data, "missing") is None
        assert safe_get(data, "missing", "default") == "default"

    def test_empty_dict(self):
        """Empty dict should return default."""
        assert safe_get({}, "any.key", "default") == "default"


class TestFormatToolSummary:
    """Test cases for format_tool_summary function."""

    def test_basic_formatting(self):
        """Tool should be formatted correctly."""
        tool = {
            "name": "TestTool",
            "category": "LLM",
            "description": "A test tool",
            "pricing": "Free",
        }
        result = format_tool_summary(tool)
        assert "TestTool" in result
        assert "LLM" in result
        assert "Free" in result

    def test_missing_fields(self):
        """Missing fields should use defaults."""
        tool = {}
        result = format_tool_summary(tool)
        assert "Unknown" in result


class TestParseQueryIntent:
    """Test cases for parse_query_intent function."""

    def test_comparison_detected(self):
        """Comparison queries should be detected."""
        intent = parse_query_intent("Compare OpenAI vs Anthropic")
        assert intent["is_comparison"] is True

    def test_recommendation_detected(self):
        """Recommendation queries should be detected."""
        intent = parse_query_intent("What's the best vector database?")
        assert intent["is_recommendation"] is True

    def test_definition_detected(self):
        """Definition queries should be detected."""
        intent = parse_query_intent("What is RAG?")
        assert intent["is_definition"] is True

    def test_free_filter_detected(self):
        """Free preference should be detected."""
        intent = parse_query_intent("Best free LLM")
        assert intent["wants_free"] is True

    def test_open_source_detected(self):
        """Open source preference should be detected."""
        intent = parse_query_intent("Best open source embedding model")
        assert intent["wants_open_source"] is True


class TestValidateToolData:
    """Test cases for validate_tool_data function."""

    def test_valid_tool_no_errors(self):
        """Valid tool should return no errors."""
        tool = {
            "name": "Valid Tool",
            "category": "LLM",
            "description": "A valid description for this tool",
        }
        errors = validate_tool_data(tool)
        assert len(errors) == 0

    def test_missing_name(self):
        """Missing name should return error."""
        tool = {"category": "LLM", "description": "Test"}
        errors = validate_tool_data(tool)
        assert any("name" in e.lower() for e in errors)

    def test_short_description(self):
        """Short description should return error."""
        tool = {"name": "Test", "category": "LLM", "description": "Short"}
        errors = validate_tool_data(tool)
        assert any("short" in e.lower() for e in errors)

    def test_invalid_category(self):
        """Invalid category should return error."""
        tool = {
            "name": "Test",
            "category": "InvalidCategory",
            "description": "A valid description",
        }
        errors = validate_tool_data(tool)
        assert any("category" in e.lower() for e in errors)
