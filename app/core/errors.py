from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.core.logging import emit_log


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def error_response(code: str, message: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}},
    )


def _validation_message(exc: RequestValidationError) -> str:
    first_error = exc.errors()[0] if exc.errors() else None
    if not first_error:
        return "invalid request"

    location = first_error.get("loc", [])
    if len(location) >= 2 and location[-1] == "prompt":
        error_type = first_error.get("type", "")
        if "missing" in error_type:
            return "prompt is required"
        if "string_type" in error_type:
            return "prompt must be a string"

    custom_message = first_error.get("msg")
    if custom_message and custom_message.startswith("Value error, "):
        return custom_message.replace("Value error, ", "", 1)
    if custom_message:
        return custom_message

    return "invalid request"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        emit_log(
            "WARNING",
            path=request.url.path,
            status_code=exc.status_code,
            error_code=exc.code,
            message=exc.message,
        )
        return error_response(exc.code, exc.message, exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        message = _validation_message(exc)
        emit_log(
            "WARNING",
            path=request.url.path,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            error_code="invalid_request",
            message=message,
        )
        return error_response("invalid_request", message, status.HTTP_422_UNPROCESSABLE_CONTENT)

    @app.exception_handler(404)
    async def handle_not_found(request: Request, __: Exception) -> JSONResponse:
        emit_log(
            "WARNING",
            path=request.url.path,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="not_found",
            message="resource not found",
        )
        return error_response("not_found", "resource not found", status.HTTP_404_NOT_FOUND)

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        emit_log(
            "ERROR",
            path=request.url.path,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="internal_error",
            message=str(exc),
        )
        return error_response("internal_error", "internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR)
