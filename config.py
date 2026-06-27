"""
Centralized configuration for the entire AI Engineer repo.

Reads all settings from the root .env file via pydantic-settings.
Import `settings` from any module or notebook:

    from config import settings

    client = Anthropic(api_key=settings.anthropic_api_key)
    model  = settings.claude_model
"""

import os
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Anchored to file location so .env is found regardless of working directory.
# Override with ENV_FILE env var to switch environments:
#   ENV_FILE=.env.staging uv run claude-certification/main.py
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # silently ignore unrecognized env vars
    )

    # --- Anthropic ---
    anthropic_api_key: str = Field(default="", description="Anthropic secret key")
    claude_model: str = Field(
        default="claude-sonnet-4-5",
        description="Claude model identifier",
    )

    # --- Runtime ---
    use_uv: bool = Field(
        default=True,
        description="Use `uv run` instead of bare `python` to launch sub-processes",
    )

    # --- OpenAI (optional) ---
    openai_api_key: str = Field(default="", description="OpenAI API key (optional)")

    # --- HuggingFace (optional) ---
    huggingface_token: str = Field(
        default="", description="HuggingFace token (optional)"
    )

    @field_validator("anthropic_api_key")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError(
                "ANTHROPIC_API_KEY is not set. "
                "Copy .env.example → .env at the repo root and fill in your key."
            )
        return v


# Singleton — import this everywhere
settings = Settings()
