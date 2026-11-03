"""Real PostgreSQL connectivity smoke test (requires DATABASE_URL)."""

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from nexora_platform.foundation.config import get_settings


@pytest.mark.integration
def test_postgresql_connection_executes_select_one() -> None:
    """Connect to configured PostgreSQL and execute SELECT 1."""
    try:
        database_url = get_settings().database_url
    except ValidationError:
        pytest.skip("DATABASE_URL is not configured; PostgreSQL connection was not tested")

    if not database_url.startswith(("postgresql://", "postgresql+psycopg://")):
        pytest.fail("DATABASE_URL must use PostgreSQL (postgresql:// or postgresql+psycopg://)")

    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar_one()
            assert result == 1, "PostgreSQL SELECT 1 returned an unexpected value"
    except SQLAlchemyError as exc:
        pytest.fail(f"PostgreSQL is unavailable or DATABASE_URL is invalid: {exc}")
    finally:
        engine.dispose()
