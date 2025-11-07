"""
Custom exception classes for Academic Research Copilot.

This module defines application-specific exceptions for better error handling
and clearer error messages throughout the application.
"""


class AcademicCopilotException(Exception):
    """Base exception for all Academic Research Copilot errors."""
    
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class MindsDBConnectionError(AcademicCopilotException):
    """Raised when unable to connect to MindsDB server."""
    
    def __init__(self, url: str, details: str = None):
        message = f"Failed to connect to MindsDB at {url}"
        super().__init__(message, details)
        self.url = url


class KnowledgeBaseError(AcademicCopilotException):
    """Raised when Knowledge Base operations fail."""
    
    def __init__(self, kb_name: str, operation: str, details: str = None):
        message = f"Knowledge Base '{kb_name}' {operation} failed"
        super().__init__(message, details)
        self.kb_name = kb_name
        self.operation = operation


class DatabaseConnectionError(AcademicCopilotException):
    """Raised when database connection fails."""
    
    def __init__(self, db_name: str, db_type: str = "DuckDB", details: str = None):
        message = f"{db_type} database '{db_name}' connection failed"
        super().__init__(message, details)
        self.db_name = db_name
        self.db_type = db_type


class QueryError(AcademicCopilotException):
    """Raised when a database query fails."""
    
    def __init__(self, query_type: str, details: str = None):
        message = f"{query_type} query failed"
        super().__init__(message, details)
        self.query_type = query_type


class ValidationError(AcademicCopilotException):
    """Raised when input validation fails."""
    
    def __init__(self, field: str, value: any, reason: str):
        message = f"Invalid {field}"
        details = f"Value '{value}' is invalid: {reason}"
        super().__init__(message, details)
        self.field = field
        self.value = value
        self.reason = reason


class PaperNotFoundError(AcademicCopilotException):
    """Raised when a requested paper is not found."""
    
    def __init__(self, entry_id: str):
        message = f"Paper with ID '{entry_id}' not found"
        super().__init__(message)
        self.entry_id = entry_id


class EmbeddingError(AcademicCopilotException):
    """Raised when embedding generation fails."""
    
    def __init__(self, model: str, details: str = None):
        message = f"Embedding generation with {model} failed"
        super().__init__(message, details)
        self.model = model


class APIKeyError(AcademicCopilotException):
    """Raised when API key is missing or invalid."""
    
    def __init__(self, service: str, details: str = None):
        message = f"{service} API key error"
        super().__init__(message, details)
        self.service = service


class DataIngestionError(AcademicCopilotException):
    """Raised when paper ingestion from ArXiv fails."""
    
    def __init__(self, source: str = "ArXiv", details: str = None):
        message = f"Failed to ingest papers from {source}"
        super().__init__(message, details)
        self.source = source
