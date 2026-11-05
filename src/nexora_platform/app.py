"""FastAPI application entry point."""

from fastapi import FastAPI

from nexora_platform.foundation.config import get_settings
from nexora_platform.foundation.health import router as health_router

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(health_router)
