from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class InferenceResult:
    request_id: str
    output: str


def generate_output(prompt: str) -> InferenceResult:
    return InferenceResult(
        request_id=f"req_{uuid4().hex[:8]}",
        output=f"Mock response for: {prompt}",
    )
