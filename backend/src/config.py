"""Pydantic settings for ToolChain backend."""

from functools import cached_property
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API Keys
    openai_api_key: str | None = None
    groq_api_key: str | None = None
    zhipu_api_key: str | None = None
    tavily_api_key: str | None = None

    # LangSmith (optional but recommended)
    langchain_tracing_v2: bool = False
    langchain_api_key: str | None = None
    langchain_project: str = "toolchain"

    # App Config
    debug: bool = False
    chroma_persist_path: str = "./chroma_db"

    # API Config - store as string to avoid JSON parsing issues
    cors_origins_str: str = "http://localhost:3000,https://toolchain.vercel.app"
    rate_limit_per_minute: int = 60

    # Error Tracking
    sentry_dsn: str | None = None

    # Caching
    redis_url: str = "memory://"

    # Embeddings
    allow_fake_embeddings: bool = False

    @property
    def cors_origins(self) -> list[str]:
        """Parse comma-separated CORS origins."""
        return [origin.strip() for origin in self.cors_origins_str.split(",") if origin.strip()]


settings = Settings()
