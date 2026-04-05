"""Structured JSON logging middleware."""

import json
import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("llm-gateway")


def emit_log(level: str, **fields: object) -> None:
    payload = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": level,
        **fields,
    }
    logger.log(getattr(logging, level, logging.INFO), json.dumps(payload, default=str))


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.time()
        response = await call_next(request)
        latency_ms = (time.time() - start) * 1000

        cache_header = response.headers.get("x-cache")
        cache_status = cache_header.lower() if cache_header else "n/a"

        emit_log(
            "INFO",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            latency_ms=round(latency_ms, 2),
            cache=cache_status,
            request_id=response.headers.get("x-request-id"),
            served_by=response.headers.get("x-served-by"),
        )

        return response


def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    root = logging.getLogger("llm-gateway")
    root.setLevel(logging.INFO)
    root.addHandler(handler)
    root.propagate = False
