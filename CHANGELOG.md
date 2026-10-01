# Changelog

All notable changes to **GST Reconciler** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-01

### Added
- **Core Engine**: Multi-tier reconciliation engine supporting Level 1 Exact, Level 2 Strong, Level 3 Normalized, and Level 4 Fuzzy match levels.
- **Normalization Layer**: Indian GSTIN validation (15-character checksum), invoice number cleaning (special character and leading zero handling), and standardized date parsing.
- **Ingestion Pipeline**: Native Excel (.xlsx, .xls) multi-sheet parser, CSV reader with auto-delimiter/encoding detection, and PDF text/scanned extraction.
- **Modular OCR**: `OCRProvider` interface with PyTesseract, PDFPlumber, and fallback extraction.
- **Smart Column Mapper**: Automatic header recognition engine with confidence metrics and profile persistence (Tally, Busy, GSTR-2B, SAP, Zoho).
- **Desktop UI**: Native PySide6 user interface featuring:
  - Executive Financial Dashboard with ITC metrics.
  - Multi-step Import Wizard.
  - Dynamic virtualized Issue Explorer with 16+ filterable discrepancy categories.
  - Side-by-side comparison modal with inline difference highlighting.
  - Manual review resolution states (Reviewed, Accepted, Rejected, Ignored).
  - Settings dialog for tax tolerances and fuzzy thresholds.
  - Built-in Demo Data loader.
- **Persistence**: ACID-compliant SQLite local database with automated migration system.
- **Export Engine**: Formatted multi-tab Excel workbooks, itemized CSVs, and audit summaries.
- **CLI Interface**: Headless CLI tool (`gst-reconciler reconcile ...`) for CI/CD and script automation.
- **Deployment**: PyInstaller packaging specification and Inno Setup Windows installer generation.
- **Documentation**: Exhaustive 12-section technical documentation suite and Architecture Decision Records (ADRs).
