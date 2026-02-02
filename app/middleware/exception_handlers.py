import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for unexpected exceptions.

    Logs:
        - Full stack trace for debugging.

    Response:
        - 500 Internal Server Error with safe, generic message.
    """
    logger.error(
        "Unhandled exception occurred",
        exc_info=True,
        extra={"path": request.url.path, "method": request.method},
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "detail": "An unexpected error occurred. Please try again later.",
        },
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """
    Handler for built-in HTTP exceptions raised explicitly with `HTTPException`.

    Response:
        - Uses the status code and message provided by the exception.
    """
    logger.warning(
        "HTTP exception",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "detail": exc.detail,
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handler for data validation errors (body, query params, path params).

    Triggered when:
        - Pydantic validation fails
        - Missing required fields
        - Incorrect data types
        - Invalid query/path params

    Response:
        - Returns 422 with error details from FastAPI/Pydantic.
    """
    logger.info(
        "Validation error",
        extra={
            "errors": exc.errors(),
            "body": await request.body(),
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "detail": exc.errors(),
        },
    )
