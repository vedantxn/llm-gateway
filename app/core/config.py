import os


def _env(key: str, default: str) -> str:
    return os.environ.get(key, default)


class Settings:
    def __init__(self) -> None:
        self.app_name: str = "llm-gateway"
        self.environment: str = _env("ENVIRONMENT", "development")
        self.max_prompt_length: int = 1000
        self.redis_url: str = _env("REDIS_URL", "redis://localhost:6379/0")
        self.mock_processing_delay_ms: int = int(_env("MOCK_PROCESSING_DELAY_MS", "50"))
        self.discord_webhook_url: str = _env("DISCORD_WEBHOOK_URL", "")


settings = Settings()
