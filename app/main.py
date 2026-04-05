import time

from fastapi import FastAPI, Response

from app.api.routes import router
from app.core.config import settings
from app.core.errors import register_exception_handlers
from app.core.logging import StructuredLoggingMiddleware, setup_logging
from app.core.metrics import registry


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.app_name)
    register_exception_handlers(app)
    app.add_middleware(StructuredLoggingMiddleware)
    app.include_router(router)

    @app.middleware("http")
    async def track_metrics(request, call_next):
        start = time.time()
        response = await call_next(request)
        latency_s = time.time() - start

        is_error = response.status_code >= 400
        cache_hit = None
        cache_header = response.headers.get("x-cache")
        if cache_header == "HIT":
            cache_hit = True
        elif cache_header == "MISS":
            cache_hit = False

        registry.inc_request(
            endpoint=request.url.path,
            latency_s=latency_s,
            is_error=is_error,
            cache_hit=cache_hit,
        )

        return response

    @app.get("/metrics")
    def metrics():
        return Response(content=registry.render(), media_type="text/plain; version=0.0.4")

    return app


app = create_app()
