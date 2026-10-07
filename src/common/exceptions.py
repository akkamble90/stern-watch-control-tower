class ControlTowerBaseException(Exception):
    """Base exception class for all Stern-Watch exceptions."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class DatabaseConnectionError(ControlTowerBaseException):
    """Raised when connections to Neo4j, Postgres, or Redis fail."""
    pass


class IngestionPipelineError(ControlTowerBaseException):
    """Raised during PySpark or Kafka streaming ingestion failures."""
    pass


class AgentExecutionError(ControlTowerBaseException):
    """Raised when a LangGraph node fails or exceeds max cyclical retries."""
    pass


class SecurityViolationError(ControlTowerBaseException):
    """Raised when HMAC signature verification fails or unauthorized actions are attempted."""
    pass


class PowerBIAuthError(ControlTowerBaseException):
    """Raised when Azure AD token generation or Power BI API calls fail."""
    pass