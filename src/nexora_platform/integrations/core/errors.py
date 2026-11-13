"""Safe, typed framework errors for integration internals."""


class IntegrationError(Exception):
    """Base class for errors safe to classify at the integration boundary."""

    code = "integration_error"


class ConnectorNotFoundError(IntegrationError):
    code = "connector_not_found"


class ConnectorAlreadyRegisteredError(IntegrationError):
    code = "connector_already_registered"


class UnsupportedCapabilityError(IntegrationError):
    code = "unsupported_capability"


class InvalidConnectorError(IntegrationError):
    code = "invalid_connector"
