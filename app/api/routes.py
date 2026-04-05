import hashlib
import socket

from fastapi import APIRouter, Response

from app.schemas.generate import GenerateRequest, GenerateResponse, HealthResponse
from app.services.cache import cache_get, cache_set
from app.services.inference import generate_output, new_request_id

router = APIRouter()


def _cache_key(prompt: str) -> str:
    return f"gen:{hashlib.sha256(prompt.encode()).hexdigest()}"


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest, response: Response) -> GenerateResponse:
    key = _cache_key(request.prompt)
    response.headers["X-Served-By"] = socket.gethostname()

    cached = cache_get(key)
    if cached is not None:
        request_id = new_request_id()
        response.headers["X-Cache"] = "HIT"
        response.headers["X-Request-Id"] = request_id
        return GenerateResponse(id=request_id, output=cached["output"], cached=True)

    result = generate_output(request.prompt)
    cache_set(key, {"output": result.output})
    response.headers["X-Cache"] = "MISS"
    response.headers["X-Request-Id"] = result.request_id

    return GenerateResponse(
        id=result.request_id,
        output=result.output,
        cached=False,
    )
