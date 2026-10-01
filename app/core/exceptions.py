"""GST Reconciler - Core Domain Exceptions."""

class GSTReconcilerError(Exception):
    """Base exception for all domain and application errors."""
    def __init__(self, message: str, user_friendly_message: str | None = None):
        super().__init__(message)
        self.user_friendly_message = user_friendly_message or message


class IngestionError(GSTReconcilerError):
    """Raised when an error occurs during file parsing or ingestion."""
    pass


class UnsupportedFileFormatError(IngestionError):
    """Raised when an uploaded file extension or mime type is not supported."""
    pass


class ColumnMappingError(GSTReconcilerError):
    """Raised when required canonical columns cannot be resolved."""
    pass


class NormalizationError(GSTReconcilerError):
    """Raised when an unexpected error occurs during data standardization."""
    pass


class ReconciliationError(GSTReconcilerError):
    """Raised when reconciliation engine fails to process candidate records."""
    pass


class DatabaseError(GSTReconcilerError):
    """Raised when local SQLite persistence operations fail."""
    pass


class OCRError(GSTReconcilerError):
    """Raised when OCR extraction fails."""
    pass


class ExportError(GSTReconcilerError):
    """Raised when generating Excel or CSV export fails."""
    pass
