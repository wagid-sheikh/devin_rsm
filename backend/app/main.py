from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.api.routers import auth, companies, cost_centers, customers, items, service_types, stores, users
from app.core.config import settings
from app.core.exceptions import (
    BusinessLogicError,
    business_logic_error_handler,
    generic_exception_handler,
    integrity_error_handler,
    validation_error_handler,
)
from app.core.logging import get_logger, setup_logging
from app.db.session import AsyncSessionLocal

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    logger.info("Starting up TSV-RSM Backend")
    yield
    logger.info("Shutting down TSV-RSM Backend")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_exception_handler(IntegrityError, integrity_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(ValidationError, validation_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(BusinessLogicError, business_logic_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, generic_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(companies.router, prefix=settings.API_V1_STR)
app.include_router(cost_centers.router, prefix=settings.API_V1_STR)
app.include_router(customers.router, prefix=settings.API_V1_STR)
app.include_router(items.router, prefix=settings.API_V1_STR)
app.include_router(service_types.router, prefix=settings.API_V1_STR)
app.include_router(stores.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


@app.get("/ready")
async def readiness_check() -> dict[str, str]:
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return {"status": "not ready", "database": "disconnected", "error": str(e)}


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "TSV-RSM Backend API", "version": settings.VERSION}
