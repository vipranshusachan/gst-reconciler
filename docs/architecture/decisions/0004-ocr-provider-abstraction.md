# ADR 0004: Modular OCR Provider Abstraction

## Status
Accepted

## Context
A significant portion of incoming invoices are received as scanned PDFs or image formats (PNG, JPG, TIFF). While most digital workflows use Excel/CSV exports from GSTN or ERPs, desktop reconciliation must gracefully handle scanned vouchers.

Challenges:
- Different users have different local environments (some have Tesseract installed, some have GPU acceleration for EasyOCR / PaddleOCR, and some cannot install large C++ runtimes).
- OCR engines vary significantly in speed, accuracy, and dependency footprint.
- Scanned text contains OCR artifacts (e.g., mistaking '8' for 'B' in GSTINs, or '0' for 'O' in invoice numbers).

## Decision
1. Implement a **Provider Pattern** (`OCRProvider` abstract base class) defining:
   - `extract_text(document: Path | bytes) -> OCRResult`
   - `extract_fields(document: Path | bytes) -> InvoiceFieldsResult`
   - `is_available() -> bool`
2. Implement **TesseractOCRProvider** as default local provider with pytesseract.
3. Implement **PDFPlumberProvider** for high-fidelity direct text extraction from vector/digital PDFs (bypassing OCR when digital text exists).
4. Implement a **Validation & Repair Pipeline**: Post-processing step that validates 15-character GSTIN checksums and repairs common OCR misreads (0/O, 1/I/l, 8/B).

## Consequences
- Clean architecture: Application does not crash if an OCR binary is absent; it reports engine availability and offers digital extraction.
- User can toggle between providers or configure custom OCR binary paths in Settings.
