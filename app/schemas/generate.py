from pydantic import BaseModel, Field, field_validator

from app.core.config import settings
class HealthResponse(BaseModel):
    status: str


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Prompt text to process")

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        trimmed = value.strip()

        if not trimmed:
            raise ValueError("prompt must not be empty")

        if len(trimmed) > settings.max_prompt_length:
            raise ValueError(f"prompt must be at most {settings.max_prompt_length} characters")

        return trimmed


class GenerateResponse(BaseModel):
    id: str
    output: str
    cached: bool
