"""Configuration settings for the MCP server."""

import os
from functools import lru_cache
from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings."""

    # Server configuration
    host: str = os.getenv("MCP_HOST", "0.0.0.0")
    port: int = int(os.getenv("MCP_PORT", "8080"))
    debug: bool = os.getenv("MCP_DEBUG", "False").lower() == "true"

    # Authentication
    auth_enabled: bool = os.getenv("MCP_AUTH_ENABLED", "False").lower() == "true"
    jwt_secret: str = os.getenv("MCP_JWT_SECRET", "")
    jwt_algorithm: str = os.getenv("MCP_JWT_ALGORITHM", "HS256")
    jwt_expiration: int = int(os.getenv("MCP_JWT_EXPIRATION", "3600"))

    # Storage
    persistence_enabled: bool = (
        os.getenv("MCP_PERSISTENCE_ENABLED", "False").lower() == "true"
    )
    storage_path: str = os.getenv("MCP_STORAGE_PATH", "./data")

    # Monitoring
    telemetry_enabled: bool = (
        os.getenv("MCP_TELEMETRY_ENABLED", "False").lower() == "true"
    )
    otlp_endpoint: str = os.getenv("MCP_OTLP_ENDPOINT", "")


@lru_cache()
def get_settings() -> Settings:
    """Return the application settings."""
    return Settings()
