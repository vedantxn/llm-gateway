from dataclasses import dataclass
from time import sleep
from uuid import uuid4

from app.core.config import settings


@dataclass(frozen=True)
class InferenceResult:
    request_id: str
    output: str


def generate_output(prompt: str) -> InferenceResult:
    # Simulate upstream work so cache hits have a visible performance benefit.
    sleep(settings.mock_processing_delay_ms / 1000)
    return InferenceResult(
        request_id=f"req_{uuid4().hex[:8]}",
        output=f"Mock response for: {prompt}",
    )
