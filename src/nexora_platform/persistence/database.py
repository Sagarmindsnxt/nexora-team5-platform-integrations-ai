"""Shared synchronous SQLAlchemy engine and session dependency."""

from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from nexora_platform.foundation.config import get_settings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Create one process-wide engine using the configured database URL."""
    return create_engine(
        get_settings().database_url,
        pool_pre_ping=True,
    )


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    """Return the process-wide SQLAlchemy session factory."""
    return sessionmaker(
        bind=get_engine(),
        autoflush=False,
        expire_on_commit=False,
    )


def get_db() -> Generator[Session, None, None]:
    """Yield a request-scoped session and always close its transaction/session."""
    session = get_session_factory()()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
