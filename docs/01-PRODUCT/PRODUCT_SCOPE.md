# Product Scope & Roadmap

## 1. Current In-Scope Capabilities (v1.0 MVP)

* **Local Offline Processing**: 100% execution on local Windows machine without network dependency.
* **File Ingestion**:
  * Microsoft Excel (.xlsx, .xls) with multi-sheet auto-discovery and preview.
  * Delimited text files (.csv, .tsv) with automatic delimiter detection (comma, semicolon, pipe, tab) and encoding fallback.
  * Native digital PDF document extraction via layout analysis.
  * Scanned PDF and image vouchers via modular OCR engine (Tesseract fallback / PyTesseract).
* **Column Mapping**:
  * Pre-trained heuristic rules for Indian GST attributes.
  * Custom mapping UI with preview of mapped columns and data samples.
  * Named profile persistence (e.g., Tally, Zoho, Busy, GSTR-2B Portal JSON/Excel).
* **Canonical Normalization**:
  * GSTIN standard uppercase alphanumeric validation.
  * Alphanumeric invoice standard formatting with leading-zero trimming.
  * Multi-format date standardization to ISO-8601.
  * Exact decimal currency arithmetic.
* **Reconciliation Engine**:
  * 4-tier matching algorithm (Exact, Strong, Normalized, Gated Fuzzy).
  * Duplicate identification across supplier GSTIN and invoice numbers.
  * Configurable penny tolerances for taxable amount, tax components, and invoice total.
  * Fine-grained categorization of 16 discrepancy types.
  * Human-readable explanations for every match decision.
* **Desktop UI & Presentation**:
  * PySide6 native desktop UI with executive metrics.
  * Virtualized table views handling 100,000+ rows smoothly.
  * Side-by-side comparison modal with color-highlighted differences.
  * Manual review actions (Open, Reviewed, Accepted, Rejected, Ignored).
* **Exporting**:
  * Formatted multi-sheet Excel reports with executive summaries, matched sheets, and itemized discrepancy sheets.
  * CSV batch export.
* **Session Persistence & Safety**:
  * SQLite database in user AppData folder with atomic transactions.
  * Project save, reload, and historical run tracking.

---

## 2. Out-of-Scope for Initial Version (Future Roadmap)

* Direct live API integration with GSTN Portal / E-Way Bill Portal (requires GST Suvidha Provider / GSP credentials and OTP infrastructure; planned for v2.0).
* Cloud database synchronization or multi-user concurrent networked editing (initial product is strictly private local desktop).
* Direct automated database writes back into proprietary accounting software (Tally ODBC / SAP RFC direct mutation); export files serve as the bridge.
* Advanced deep-learning OCR training models (system uses standard Tesseract and layout extraction).
