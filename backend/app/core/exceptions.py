from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.core.logging import get_logger

logger = get_logger(__name__)


class ErrorResponse:
    def __init__(
        self,
        type_: str,
        title: str,
        status_code: int,
        detail: str,
        instance: str,
        extra: dict[str, Any] | None = None,
    ):
        self.type = type_
        self.title = title
        self.status = status_code
        self.detail = detail
        self.instance = instance
        self.extra = extra or {}

    def to_dict(self) -> dict[str, Any]:
        response = {
            "type": self.type,
            "title": self.title,
            "status": self.status,
            "detail": self.detail,
            "instance": self.instance,
        }
        response.update(self.extra)
        return response


class BusinessLogicError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str | None = None,
        extra: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "business_logic_error"
        self.extra = extra or {}
        super().__init__(self.message)


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    detail = str(exc.orig) if hasattr(exc, "orig") else str(exc)

    field_name = None
    field_value = None

    if "duplicate key value violates unique constraint" in detail:
        if 'Key (' in detail:
            try:
                key_part = detail.split('Key (')[1].split(')')[0]
                value_part = detail.split('=(')[1].split(')')[0]
                field_name = key_part
                field_value = value_part
            except (IndexError, AttributeError):
                pass

        if field_name:
            user_message = f"A record with {field_name} '{field_value}' already exists."
            extra = {"field": field_name, "value": field_value}
        else:
            user_message = "A record with this value already exists."
            extra = {}
    else:
        user_message = "Database integrity constraint violation."
        extra = {}

    logger.warning(
        f"Integrity constraint violation on {request.url.path}",
        extra={
            "request_id": request.headers.get("X-Request-ID"),
            "method": request.method,
            "path": request.url.path,
            "constraint_type": "unique" if "duplicate key" in detail else "unknown",
            "field": field_name,
        },
    )

    error_response = ErrorResponse(
        type_="https://api.tsv-rsm.com/errors/integrity-constraint",
        title="Integrity Constraint Violation",
        status_code=status.HTTP_409_CONFLICT,
        detail=user_message,
        instance=str(request.url),
        extra=extra,
    )

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_response.to_dict(),
    )


async def validation_error_handler(
    request: Request, exc: RequestValidationError | ValidationError
) -> JSONResponse:
    errors = []
    if isinstance(exc, RequestValidationError):
        for error in exc.errors():
            field_path = " -> ".join(str(loc) for loc in error["loc"])
            errors.append({
                "field": field_path,
                "message": error["msg"],
                "type": error["type"],
            })
    else:
        for error in exc.errors():
            field_path = " -> ".join(str(loc) for loc in error["loc"])
            errors.append({
                "field": field_path,
                "message": error["msg"],
                "type": error["type"],
            })

    logger.info(
        f"Validation error on {request.url.path}",
        extra={
            "request_id": request.headers.get("X-Request-ID"),
            "method": request.method,
            "path": request.url.path,
            "validation_errors": errors,
        },
    )

    error_response = ErrorResponse(
        type_="https://api.tsv-rsm.com/errors/validation-error",
        title="Validation Error",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="One or more fields failed validation.",
        instance=str(request.url),
        extra={"errors": errors},
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.to_dict(),
    )


async def business_logic_error_handler(
    request: Request, exc: BusinessLogicError
) -> JSONResponse:
    logger.warning(
        f"Business logic error on {request.url.path}: {exc.message}",
        extra={
            "request_id": request.headers.get("X-Request-ID"),
            "method": request.method,
            "path": request.url.path,
            "error_code": exc.error_code,
        },
    )

    error_response = ErrorResponse(
        type_=f"https://api.tsv-rsm.com/errors/{exc.error_code}",
        title="Business Logic Error",
        status_code=exc.status_code,
        detail=exc.message,
        instance=str(request.url),
        extra=exc.extra,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.to_dict(),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        f"Unhandled exception on {request.url.path}: {type(exc).__name__}",
        extra={
            "request_id": request.headers.get("X-Request-ID"),
            "method": request.method,
            "path": request.url.path,
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        },
        exc_info=True,
    )

    error_response = ErrorResponse(
        type_="https://api.tsv-rsm.com/errors/internal-server-error",
        title="Internal Server Error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred. Please try again later.",
        instance=str(request.url),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.to_dict(),
    )
