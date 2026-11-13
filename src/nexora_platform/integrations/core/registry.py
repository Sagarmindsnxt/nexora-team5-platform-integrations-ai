"""In-process connector registry; no dynamic imports or provider loading."""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from nexora_platform.integrations.core.contracts import (
    Connector,
    ConnectorCapability,
    ConnectorDescriptor,
)
from nexora_platform.integrations.core.errors import (
    ConnectorAlreadyRegisteredError,
    ConnectorNotFoundError,
    InvalidConnectorError,
    UnsupportedCapabilityError,
)


class ConnectorRegistry:
    """Explicit allowlist registry for adapters constructed by application code."""

    def __init__(self) -> None:
        self._connectors: dict[str, Connector] = {}

    def register(self, connector: Connector) -> None:
        descriptor = getattr(connector, "descriptor", None)
        if not isinstance(descriptor, ConnectorDescriptor):
            raise InvalidConnectorError("connector must expose a valid descriptor")
        if descriptor.provider in self._connectors:
            raise ConnectorAlreadyRegisteredError(
                f"provider already registered: {descriptor.provider}"
            )
        self._connectors[descriptor.provider] = connector

    def get(
        self, provider: str, *, capability: ConnectorCapability | None = None
    ) -> Connector:
        try:
            connector = self._connectors[provider]
        except KeyError as exc:
            raise ConnectorNotFoundError(f"unknown provider: {provider}") from exc
        if capability is not None and capability not in connector.descriptor.capabilities:
            raise UnsupportedCapabilityError(
                f"provider {provider} does not declare {capability.value}"
            )
        return connector

    def descriptors(self) -> tuple[ConnectorDescriptor, ...]:
        return tuple(
            sorted(
                (connector.descriptor for connector in self._connectors.values()),
                key=lambda item: item.provider,
            )
        )

    @property
    def connectors(self) -> Mapping[str, Connector]:
        """Read-only view for diagnostics and application wiring."""
        return MappingProxyType(self._connectors)
