"""Unit tests for liveness and sanitized database health responses."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from nexora_platform.app import app
from nexora_platform.foundation import health
from nexora_platform.foundation.config import Settings
from nexora_platform.persistence import database


@pytest.mark.parametrize("path", ["/api/v1/health", "/health"])
def test_application_health_does_not_check_database(monkeypatch, path) -> None:
    def unexpected_database_access():
        pytest.fail("Application health must not access the database")

    monkeypatch.setattr(health, "get_engine", unexpected_database_access)
    monkeypatch.setattr(database, "create_engine", unexpected_database_access)
    response = TestClient(app).get(path)

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "application": "Nexora Team 5 Platform",
    }


@pytest.mark.parametrize("path", ["/api/v1/health/db", "/ready"])
def test_database_health_success_uses_and_closes_connection(monkeypatch, path) -> None:
    class FakeConnection:
        closed = False

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            self.closed = True

        def execute(self, statement):
            assert str(statement) == "SELECT 1"
            return self

        def scalar_one(self):
            return 1

    class FakeEngine:
        def __init__(self):
            self.connection = FakeConnection()

        def connect(self):
            return self.connection

    engine = FakeEngine()
    monkeypatch.setattr(health, "get_engine", lambda: engine)

    response = TestClient(app).get(path)

    assert response.status_code == 200
    assert response.json()["database"] == "connected"
    assert engine.connection.closed


@pytest.mark.parametrize("path", ["/api/v1/health/db", "/ready"])
def test_database_health_failure_is_sanitized(monkeypatch, path) -> None:
    class FailingEngine:
        def connect(self):
            raise OperationalError(
                "connect",
                {},
                Exception("password=secret internal-host"),
            )

    monkeypatch.setattr(health, "get_engine", lambda: FailingEngine())

    response = TestClient(app).get(path)

    assert response.status_code == 503
    assert response.json() == {
        "status": "unhealthy",
        "database": "disconnected",
        "message": "Database connection is unavailable",
    }
    assert "secret" not in response.text
    assert "internal-host" not in response.text


@pytest.mark.parametrize("path", ["/api/v1/health/db", "/ready"])
def test_missing_database_configuration_is_sanitized(monkeypatch, path) -> None:
    # Exercise the real engine helper without reading local credentials.
    settings = Settings.model_construct(database_url=None)
    monkeypatch.setattr(database, "get_settings", lambda: settings)
    database.get_engine.cache_clear()
    try:
        response = TestClient(app).get(path)
        assert response.status_code == 503
        assert response.json() == {
            "status": "unhealthy",
            "database": "disconnected",
            "message": "Database connection is unavailable",
        }
        assert "Database configuration is missing" not in response.text
    finally:
        database.get_engine.cache_clear()


@pytest.mark.parametrize("path", ["/api/v1/health/db", "/ready"])
def test_query_failure_closes_connection(monkeypatch, path) -> None:
    class FailingConnection:
        closed = False

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            self.closed = True

        def connect(self):
            return self

        def execute(self, statement):
            assert str(statement) == "SELECT 1"
            raise OperationalError("query", {}, Exception("password=secret internal-host"))

    connection = FailingConnection()
    monkeypatch.setattr(health, "get_engine", lambda: connection)
    response = TestClient(app).get(path)
    assert response.status_code == 503
    assert connection.closed
    assert "secret" not in response.text
    assert "internal-host" not in response.text


def test_version_matches_openapi_and_all_endpoints_are_registered() -> None:
    client = TestClient(app)
    response = client.get("/version")
    schema = client.get("/openapi.json").json()
    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0"}
    assert response.json()["version"] == schema["info"]["version"] == app.version
    for path in ("/health", "/ready", "/version", "/api/v1/health", "/api/v1/health/db"):
        assert "get" in schema["paths"][path]
