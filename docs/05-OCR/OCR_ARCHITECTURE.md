# Modular OCR Architecture

## 1. Provider Pattern Abstraction

The OCR subsystem is decoupled from any single concrete OCR technology. The interface is defined in `app.ocr.ocr_provider.OCRProvider`:

```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class OCRResult:
    text: str
    confidence: float
    metadata: Dict[str, Any]

class OCRProvider(ABC):
    @abstractmethod
    def extract_text(self, document_path: Path) -> OCRResult:
        """Extract text and confidence score from a document image or PDF."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if runtime dependencies (binaries/models) are present."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Provider display name."""
        pass
```

### Supported Concrete Implementations:
1. **`PDFPlumberProvider`**: Extracts structured text and tables directly from vector/digital PDF invoices (fast, 100% precision, zero OCR noise).
2. **`TesseractOCRProvider`**: Wraps Google Tesseract OCR via `pytesseract` for image scans.
3. **`MockOCRProvider`**: Used in automated CI test environments without requiring external Tesseract binaries.
