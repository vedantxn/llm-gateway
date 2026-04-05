from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.errors import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    register_exception_handlers(app)
    app.include_router(router)
    return app


app = create_app()
