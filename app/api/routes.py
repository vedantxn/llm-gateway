from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.schemas.generate import GenerateRequest, GenerateResponse, HealthResponse
from app.services.inference import generate_output

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    result = generate_output(request.prompt)
    return GenerateResponse(
        id=result.request_id,
        output=result.output,
        cached=False,
    )


@router.get("/metrics", response_class=PlainTextResponse)
def metrics() -> str:
    return 'llm_gateway_up{service="llm-gateway"} 1\n'
