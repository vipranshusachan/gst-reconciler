"""Tesseract OCR Provider."""

from pathlib import Path

from app.core.exceptions import OCRError
from app.ocr.ocr_provider import OCRProvider, OCRResult

try:
    import pytesseract
    from PIL import Image

    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False


class TesseractOCRProvider(OCRProvider):
    """Local Tesseract OCR engine implementation."""

    def __init__(self, tesseract_cmd: str = ""):
        self.tesseract_cmd = tesseract_cmd
        if tesseract_cmd and HAS_TESSERACT:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def is_available(self) -> bool:
        if not HAS_TESSERACT:
            return False
        try:
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False

    def get_name(self) -> str:
        return "Tesseract OCR"

    def extract_text(self, file_path: Path) -> OCRResult:
        if not self.is_available():
            raise OCRError(
                "Tesseract OCR engine is not installed or configured on this system.",
                user_friendly_message="OCR engine is not available. Please install Tesseract or provide digital Excel/CSV files.",
            )

        try:
            img = Image.open(file_path)
            # Perform OCR extraction
            text = pytesseract.image_to_string(img)
            # Extract confidence data
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            confs = [int(c) for c in data.get("conf", []) if str(c).isdigit() and int(c) >= 0]
            avg_conf = (sum(confs) / len(confs) / 100.0) if confs else 0.80

            return OCRResult(
                text=text,
                confidence=avg_conf,
                provider_name=self.get_name(),
                metadata={"total_words": len(confs)},
            )
        except Exception as e:
            raise OCRError(f"OCR extraction failed on {file_path.name}: {e}") from e
