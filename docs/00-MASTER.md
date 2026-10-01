# GST Reconciler — Master Documentation Index

Welcome to the comprehensive technical documentation for **GST Reconciler**, an open-source, offline-first desktop application designed for Indian businesses, tax consultants, and chartered accountants to reconcile Goods and Services Tax (GST) records with high precision.

---

## 📑 Documentation Structure

### 01. Product
* [Product Requirements](file:///docs/01-PRODUCT/PRODUCT_REQUIREMENTS.md) — Core business requirements, statutory alignment (Section 16(2)(aa) & Rule 36(4)).
* [Product Scope](file:///docs/01-PRODUCT/PRODUCT_SCOPE.md) — In-scope capabilities, boundaries, and future roadmap.
* [User Personas](file:///docs/01-PRODUCT/USER_PERSONAS.md) — Profiles of Tax Consultants, In-house Accountants, and SME Owners.
* [User Journeys](file:///docs/01-PRODUCT/USER_JOURNEYS.md) — Step-by-step paths from file ingestion to mismatch export.
* [Feature Matrix](file:///docs/01-PRODUCT/FEATURE_MATRIX.md) — Feature breakdown across functional modules.

### 02. Architecture
* [System Architecture](file:///docs/02-ARCHITECTURE/SYSTEM_ARCHITECTURE.md) — High-level architecture, boundaries, clean modular layers.
* [Application Architecture](file:///docs/02-ARCHITECTURE/APPLICATION_ARCHITECTURE.md) — Desktop client structure, UI threading, async workers.
* [Module Architecture](file:///docs/02-ARCHITECTURE/MODULE_ARCHITECTURE.md) — Ingestion, Normalization, Engine, Persistence, and Reporting modules.
* [Data Flow](file:///docs/02-ARCHITECTURE/DATA_FLOW.md) — End-to-end data pipelines from disk to dashboard.
* [Security Architecture](file:///docs/02-ARCHITECTURE/SECURITY_ARCHITECTURE.md) — Zero-telemetry, offline-first, local isolation.
* [Performance Architecture](file:///docs/02-ARCHITECTURE/PERFORMANCE_ARCHITECTURE.md) — Processing strategies for 100k+ record sets, memory bounds, vectorized operations.

### 03. Data & Formats
* [Data Model](file:///docs/03-DATA/DATA_MODEL.md) — Canonical Invoice entity, source metadata, and match ledger schema.
* [Input Formats](file:///docs/03-DATA/INPUT_FORMATS.md) — Excel (.xlsx/.xls), CSV, PDF (text & scan), and image specifications.
* [Column Mapping](file:///docs/03-DATA/COLUMN_MAPPING.md) — Heuristic detection algorithms, confidence scoring, profile reuse.
* [Normalization](file:///docs/03-DATA/NORMALIZATION.md) — GSTIN sanitation, invoice numbering rules, date normalization, preserving raw values.
* [Reconciliation Model](file:///docs/03-DATA/RECONCILIATION_MODEL.md) — Match states, difference models, and audit records.

### 04. Reconciliation Engine
* [Matching Engine](file:///docs/04-RECONCILIATION/MATCHING_ENGINE.md) — Multi-pass matching pipeline architecture.
* [Matching Rules](file:///docs/04-RECONCILIATION/MATCHING_RULES.md) — Level 1 Exact, Level 2 Strong, Level 3 Normalized, Level 4 Fuzzy.
* [Fuzzy Matching](file:///docs/04-RECONCILIATION/FUZZY_MATCHING.md) — Levenshtein, Token Sort, and Jaro-Winkler with strict score gates.
* [Tax Calculation](file:///docs/04-RECONCILIATION/TAX_CALCULATION.md) — Configurable tolerances (₹1–₹10), rounding differences, rate checks.
* [Mismatch Classification](file:///docs/04-RECONCILIATION/MISMATCH_CLASSIFICATION.md) — Taxonomy of 16+ discrepancy types.
* [Reconciliation Workflow](file:///docs/04-RECONCILIATION/RECONCILIATION_WORKFLOW.md) — Execution steps, worker thread lifecycle, signal dispatch.

### 05. OCR Pipeline
* [OCR Architecture](file:///docs/05-OCR/OCR_ARCHITECTURE.md) — Decoupled provider interface pattern.
* [OCR Pipeline](file:///docs/05-OCR/OCR_PIPELINE.md) — Preprocessing (deskew, binarize), bounding box extraction, regex extraction.
* [Document Types](file:///docs/05-OCR/DOCUMENT_TYPES.md) — Tax Invoices, Credit Notes, Debit Notes, Bill of Entry.
* [OCR Validation](file:///docs/05-OCR/OCR_VALIDATION.md) — Checksum and regex verification, confidence scoring.

### 06. User Interface & Experience
* [UI Architecture](file:///docs/06-UI/UI_ARCHITECTURE.md) — PySide6 / Qt architecture, Model-View-Presenter separation.
* [Design System](file:///docs/06-UI/DESIGN_SYSTEM.md) — Financial palette, typography, status badges, contrast guidelines.
* [Screen List](file:///docs/06-UI/SCREEN_LIST.md) — Specifications for all application screens.
* [Dashboard](file:///docs/06-UI/DASHBOARD.md) — Key metrics, ITC at risk, discrepancy distribution charts.
* [UX Flows](file:///docs/06-UI/UX_FLOWS.md) — Wizard workflows, side-by-side inspection, resolution states.

### 07. Internal APIs
* [Internal APIs](file:///docs/07-API/INTERNAL_APIS.md) — Python programmatic service interface and CLI integration.

### 08. Testing & Quality Assurance
* [Test Strategy](file:///docs/08-TESTING/TEST_STRATEGY.md) — Test pyramid, unit, integration, stress, and golden dataset testing.
* [Test Cases](file:///docs/08-TESTING/TEST_CASES.md) — Exhaustive test matrix.
* [Reconciliation Test Data](file:///docs/08-TESTING/RECONCILIATION_TEST_DATA.md) — Synthetic test data generators.
* [QA Checklist](file:///docs/08-TESTING/QA_CHECKLIST.md) — Release readiness gate checklist.

### 09. Deployment & Packaging
* [Windows Build](file:///docs/09-DEPLOYMENT/WINDOWS_BUILD.md) — PyInstaller specification, hooks, reproducible builds.
* [Installer](file:///docs/09-DEPLOYMENT/INSTALLER.md) — Inno Setup script, uninstaller, shortcuts, registry entries.
* [GitHub Releases](file:///docs/09-DEPLOYMENT/GITHUB_RELEASES.md) — Release automation, asset publishing, changelog extraction.
* [Auto Update](file:///docs/09-DEPLOYMENT/AUTO_UPDATE.md) — Secure update checks, SHA-256 verification, user prompt.
* [CI/CD](file:///docs/09-DEPLOYMENT/CI_CD.md) — GitHub Actions multi-stage build, test, and release workflow.

### 10. Security & Privacy
* [Security](file:///docs/10-SECURITY/SECURITY.md) — Security policies, memory safety, dependency audit.
* [Data Privacy](file:///docs/10-SECURITY/DATA_PRIVACY.md) — Complete offline isolation guarantee, local SQLite storage.
* [Threat Model](file:///docs/10-SECURITY/THREAT_MODEL.md) — STRIDE analysis on desktop files, update feeds, and temp directories.

### 11. Developer Guide
* [Development Setup](file:///docs/11-DEVELOPER/DEVELOPMENT_SETUP.md) — Virtualenv, dependencies, IDE configurations.
* [Contributing](file:///docs/11-DEVELOPER/CONTRIBUTING.md) — Code style, pull request guidelines, commit standards.
* [Code Style](file:///docs/11-DEVELOPER/CODE_STYLE.md) — Ruff, Mypy strict mode, formatting conventions.
* [Debugging](file:///docs/11-DEVELOPER/DEBUGGING.md) — Diagnostic flags, profiling runs, debug logging.

### 12. End-User Guide
* [User Guide](file:///docs/12-USER/USER_GUIDE.md) — Comprehensive operation manual.
* [Installation](file:///docs/12-USER/INSTALLATION.md) — Step-by-step Windows installation.
* [Quick Start](file:///docs/12-USER/QUICK_START.md) — 5-minute walkthrough from import to export.
* [FAQ](file:///docs/12-USER/FAQ.md) — Frequently asked questions regarding GST reconciliation.
* [Troubleshooting](file:///docs/12-USER/TROUBLESHOOTING.md) — Error resolution for common file and parsing anomalies.

### Architecture Decision Records (ADRs)
* [ADR 0001: Desktop UI Framework (PySide6 / Qt)](file:///docs/architecture/decisions/0001-desktop-ui-framework.md)
* [ADR 0002: Data Processing & Reconciliation Engine](file:///docs/architecture/decisions/0002-data-processing-engine.md)
* [ADR 0003: Storage Engine & Migration Strategy](file:///docs/architecture/decisions/0003-storage-engine.md)
* [ADR 0004: Modular OCR Provider Abstraction](file:///docs/architecture/decisions/0004-ocr-provider-abstraction.md)
* [ADR 0005: Open Source License Selection (Apache-2.0)](file:///docs/architecture/decisions/0005-license-selection.md)
