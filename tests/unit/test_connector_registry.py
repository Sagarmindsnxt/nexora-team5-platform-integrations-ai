"""Tests for the provisional, explicit connector registry."""

from dataclasses import dataclass

import pytest

from nexora_platform.integrations.core.contracts import (
    ConnectorCapability,
    ConnectorDescriptor,
    IntegrationCategory,
)
from nexora_platform.integrations.core.errors import (
    ConnectorAlreadyRegisteredError,
    ConnectorNotFoundError,
    InvalidConnectorError,
    UnsupportedCapabilityError,
)
from nexora_platform.integrations.core.registry import ConnectorRegistry


@dataclass
class FakeConnector:
    descriptor: ConnectorDescriptor


def connector(provider: str = "fake") -> FakeConnector:
    return FakeConnector(
        ConnectorDescriptor(
            provider=provider,
            version="0.1",
            categories=frozenset({IntegrationCategory.PULL_REQUEST}),
            capabilities=frozenset({ConnectorCapability.FETCH}),
        )
    )


def test_registry_registers_and_discovers_explicit_connector() -> None:
    registry = ConnectorRegistry()
    fake = connector()
    registry.register(fake)

    assert registry.get("fake") is fake
    assert registry.get("fake", capability=ConnectorCapability.FETCH) is fake
    assert registry.descriptors() == (fake.descriptor,)


def test_registry_rejects_duplicate_provider() -> None:
    registry = ConnectorRegistry()
    registry.register(connector())
    with pytest.raises(ConnectorAlreadyRegisteredError):
        registry.register(connector())


def test_registry_rejects_unknown_provider_and_capability() -> None:
    registry = ConnectorRegistry()
    with pytest.raises(ConnectorNotFoundError):
        registry.get("missing")
    registry.register(connector())
    with pytest.raises(UnsupportedCapabilityError):
        registry.get("fake", capability=ConnectorCapability.SYNC)


def test_registry_rejects_invalid_connector_and_exposes_read_only_view() -> None:
    registry = ConnectorRegistry()
    with pytest.raises(InvalidConnectorError):
        registry.register(object())  # type: ignore[arg-type]
    registry.register(connector())
    with pytest.raises(TypeError):
        registry.connectors["other"] = connector("other")  # type: ignore[index]
