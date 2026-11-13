"""Provisional shared connector types.

These types provide an internal extension seam only. They are not a published
cross-team or provider contract until the relevant owners approve the semantics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol


class IntegrationCategory(StrEnum):
    """Canonical categories named by the Team 5 requirements."""

    PULL_REQUEST = "pull_request"
    WORK_ITEM = "work_item"
    INCIDENT = "incident"


class ConnectorCapability(StrEnum):
    """Operations a provider adapter may expose."""

    AUTHENTICATE = "authenticate"
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    HEALTH_CHECK = "health_check"
    SYNC = "sync"
    FETCH = "fetch"
    WEBHOOK = "webhook"


@dataclass(frozen=True, slots=True)
class ConnectorDescriptor:
    """Static metadata used to validate and discover a connector."""

    provider: str
    version: str
    categories: frozenset[IntegrationCategory]
    capabilities: frozenset[ConnectorCapability]

    def __post_init__(self) -> None:
        if not self.provider or self.provider.strip() != self.provider:
            raise ValueError("provider must be a non-empty, trimmed identifier")
        if not self.version or self.version.strip() != self.version:
            raise ValueError("version must be a non-empty, trimmed identifier")


@dataclass(frozen=True, slots=True)
class ConnectorContext:
    """Execution context supplied by the framework, never by provider payloads."""

    integration_id: str
    organization_id: str
    correlation_id: str


@dataclass(frozen=True, slots=True)
class HealthResult:
    healthy: bool
    detail: str | None = None


@dataclass(frozen=True, slots=True)
class SyncResult:
    outcome: str
    records_seen: int = 0
    records_delivered: int = 0


@dataclass(frozen=True, slots=True)
class FetchResult:
    items: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    next_cursor: str | None = None


@dataclass(frozen=True, slots=True)
class WebhookResult:
    accepted: bool
    duplicate: bool = False


class Connector(Protocol):
    """Proposed asynchronous adapter seam; owner approval is still required."""

    descriptor: ConnectorDescriptor

    async def authenticate(self, context: ConnectorContext) -> None: ...

    async def connect(self, context: ConnectorContext) -> None: ...

    async def disconnect(self, context: ConnectorContext) -> None: ...

    async def health_check(self, context: ConnectorContext) -> HealthResult: ...

    async def sync(self, context: ConnectorContext) -> SyncResult: ...

    async def fetch(
        self, context: ConnectorContext, *, cursor: str | None = None
    ) -> FetchResult: ...

    async def handle_webhook(
        self,
        context: ConnectorContext,
        *,
        headers: dict[str, str],
        raw_body: bytes,
    ) -> WebhookResult: ...
