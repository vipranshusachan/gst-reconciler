"""Modular OCR Provider Abstraction."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict


@dataclass
class OCRResult:
    """Extracted text and metadata from an OCR scan."""

    text: str
    confidence: float = 0.0
    provider_name: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class OCRProvider(ABC):
    """Abstract OCR Provider interface."""

    @abstractmethod
    def extract_text(self, file_path: Path) -> OCRResult:
        """Extract text content from an image or scanned document."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check whether local runtime dependencies (binaries/models) are present."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return display name of the OCR engine."""
        pass
