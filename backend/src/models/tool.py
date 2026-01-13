"""AITool data model and schema definitions."""

from typing import Literal

from pydantic import BaseModel, Field


class AITool(BaseModel):
    """Represents an AI development tool in the database."""

    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Tool name")
    category: Literal[
        "api", "mcp", "sdk", "cli", "vector_db", "framework", "agent_framework"
    ] = Field(..., description="Primary category")
    subcategory: str = Field(..., description="More specific classification")
    description: str = Field(..., description="Full description for RAG")
    provider: str = Field(..., description="Company or organization")
    pricing: Literal["free", "freemium", "paid", "enterprise"] = Field(
        ..., description="Pricing model"
    )
    languages: list[str] = Field(default_factory=list, description="Supported languages")
    use_cases: list[str] = Field(default_factory=list, description="Common use cases")
    documentation_url: str = Field(..., description="Official docs URL")
    github_url: str | None = Field(None, description="GitHub repo if open source")
    npm_package: str | None = Field(None, description="NPM package name")
    pypi_package: str | None = Field(None, description="PyPI package name")
    code_example: str = Field(..., description="Quick start code snippet")
    pros: list[str] = Field(default_factory=list, description="Advantages")
    cons: list[str] = Field(default_factory=list, description="Disadvantages")
    alternatives: list[str] = Field(default_factory=list, description="Similar tools")
    popularity_score: int = Field(
        default=50, ge=0, le=100, description="Popularity 0-100"
    )


class ToolQuery(BaseModel):
    """Query parameters for searching tools."""

    category: str | None = None
    pricing: str | None = None
    language: str | None = None
    search: str | None = None
    limit: int = Field(default=20, ge=1, le=100)


class ChatMessage(BaseModel):
    """Single message in conversation history."""

    role: Literal["user", "assistant"] = Field(..., description="Message sender")
    content: str = Field(..., min_length=1, description="Message content")
    timestamp: int | None = Field(None, description="Unix timestamp")


class ChatQuery(BaseModel):
    """User query for the AI chat interface."""

    query: str = Field(..., min_length=1, max_length=1000)
    messages: list[ChatMessage] = Field(
        default_factory=list,
        description="Conversation history (optional)"
    )


class CompareRequest(BaseModel):
    """Request to compare multiple tools."""

    tool_ids: list[str] = Field(..., min_length=2, max_length=5)


class SubscribeRequest(BaseModel):
    """Email subscription request."""

    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
