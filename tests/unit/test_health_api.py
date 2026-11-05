"""Unit tests for liveness and sanitized database health responses."""

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from nexora_platform.app import app
from nexora_platform.foundation import health


def test_application_health_does_not_check_database() -> None:
    response = TestClient(app).get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "application": "Nexora Team 5 Platform",
    }


def test_database_health_success_uses_and_closes_connection(monkeypatch) -> None:
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

    response = TestClient(app).get("/api/v1/health/db")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"
    assert engine.connection.closed


def test_database_health_failure_is_sanitized(monkeypatch) -> None:
    class FailingEngine:
        def connect(self):
            raise OperationalError(
                "connect",
                {},
                Exception("password=secret internal-host"),
            )

    monkeypatch.setattr(health, "get_engine", lambda: FailingEngine())

    response = TestClient(app).get("/api/v1/health/db")

    assert response.status_code == 503
    assert response.json() == {
        "status": "unhealthy",
        "database": "disconnected",
        "message": "Database connection is unavailable",
    }
    assert "secret" not in response.text
    assert "internal-host" not in response.text
