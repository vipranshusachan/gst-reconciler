"""Modular OCR package."""

from app.ocr.ocr_provider import OCRProvider, OCRResult
from app.ocr.tesseract_ocr import TesseractOCRProvider
from app.ocr.validator import OCRFieldExtractor

__all__ = [
    "OCRProvider",
    "OCRResult",
    "TesseractOCRProvider",
    "OCRFieldExtractor",
]
