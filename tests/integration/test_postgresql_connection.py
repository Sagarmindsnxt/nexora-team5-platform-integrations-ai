"""Real PostgreSQL connectivity smoke test (requires DATABASE_URL)."""

import pytest
from fastapi.testclient import TestClient

from nexora_platform.app import app
from nexora_platform.foundation.config import get_settings


@pytest.mark.integration
def test_postgresql_connection_executes_select_one() -> None:
    """Connect to configured PostgreSQL and execute SELECT 1."""
    database_url = get_settings().database_url
    if not database_url:
        pytest.skip("DATABASE_URL is not configured; PostgreSQL connection was not tested")

    if not database_url.startswith(("postgresql://", "postgresql+psycopg://")):
        pytest.fail("DATABASE_URL must use PostgreSQL (postgresql:// or postgresql+psycopg://)")

    with TestClient(app) as client:
        response = client.get("/api/v1/health/db")

    assert response.status_code == 200, (
        "PostgreSQL health check failed; verify DATABASE_URL and database availability"
    )
    assert response.json() == {
        "status": "healthy",
        "database": "connected",
        "message": "PostgreSQL connection successful",
    }
