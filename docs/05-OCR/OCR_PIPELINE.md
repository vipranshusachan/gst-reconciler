# OCR Ingestion Pipeline

## 1. Document Extraction Pipeline

The invoice OCR pipeline operates in three stages:

```
[Scanned PDF / Image File]
            │
            ▼
[Step 1: Digital vs Scanned Detection]
    ├── Has embedded selectable text? ──► YES ──► Extract via PDFPlumber (Fast)
    └── NO / Image ─────────────────────► Preprocessing
            │
            ▼
[Step 2: Preprocessing]
    ├── Grayscale conversion
    ├── Otsu binarization (contrast enhancement)
    └── Deskewing (rotation correction)
            │
            ▼
[Step 3: OCR Engine Recognition]
    └── Tesseract OCR extraction -> Raw extracted text string
            │
            ▼
[Step 4: Regex Field Extraction]
    ├── GSTIN matcher: `\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}\b`
    ├── Invoice No matcher: `(?:Invoice|Bill|Inv)\s*(?:No|#)?[:.\s]*([A-Z0-9\/-]+)`
    ├── Date matcher: `(?:Date)[:.\s]*([0-9]{1,2}[-\/.][0-9]{1,2}[-\/.][0-9]{2,4})`
    └── Financial Amounts: Regex table parsing for Taxable, IGST, CGST, SGST, Total
            │
            ▼
[Step 5: OCR Validation & Checksum Verification]
    └── Verify GSTIN check digit & mathematical parity (Taxable + Tax == Total)
```
