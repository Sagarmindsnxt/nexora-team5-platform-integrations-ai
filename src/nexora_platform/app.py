"""FastAPI application entry point."""

from fastapi import FastAPI

from nexora_platform.foundation.config import get_settings
from nexora_platform.foundation.health import router as health_router
from nexora_platform.foundation.health import application_health, database_health

VERSION = "0.1.0"

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug, version=VERSION)
app.include_router(health_router)
app.add_api_route("/health", application_health, methods=["GET"], tags=["health"])
app.add_api_route(
    "/ready", database_health, methods=["GET"], response_model=None, tags=["health"]
)


@app.get("/version")
def version() -> dict[str, str]:
    """Return the same release version used by OpenAPI."""
    return {"version": VERSION}
