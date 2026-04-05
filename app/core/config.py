from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "llm-gateway"
    environment: str = "development"
    max_prompt_length: int = 1000


settings = Settings()
