"""Application and database health routes."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from nexora_platform.foundation.config import get_settings
from nexora_platform.persistence.database import get_engine

router = APIRouter(prefix="/api/v1/health", tags=["health"])


@router.get("")
def application_health() -> dict[str, str]:
    """Report that the API process is running without contacting PostgreSQL."""
    return {"status": "healthy", "application": get_settings().app_name}


@router.get("/db", response_model=None)
def database_health() -> dict[str, str] | JSONResponse:
    """Run a lightweight PostgreSQL query and return a sanitized status."""
    try:
        with get_engine().connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar_one()
            if result != 1:
                raise SQLAlchemyError("Health query returned an unexpected result")
    except (SQLAlchemyError, RuntimeError):
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "message": "Database connection is unavailable",
            },
        )

    return {
        "status": "healthy",
        "database": "connected",
        "message": "PostgreSQL connection successful",
    }
