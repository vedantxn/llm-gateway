import os


def _env(key: str, default: str) -> str:
    return os.environ.get(key, default)


class Settings:
    def __init__(self) -> None:
        self.app_name: str = "llm-gateway"
        self.environment: str = _env("ENVIRONMENT", "development")
        self.max_prompt_length: int = 1000
        self.redis_url: str = _env("REDIS_URL", "redis://localhost:6379/0")


settings = Settings()
