# Product Requirements Document (PRD)

## 1. Product Vision & Statutory Background

Under the Indian Goods and Services Tax (GST) regime, registered taxpayers claim Input Tax Credit (ITC) on goods and services procured for business. Section 16(2)(aa) of the CGST Act, read in conjunction with Rule 36(4), mandates that ITC can only be claimed if the details of the invoice or debit note have been furnished by the supplier in their GSTR-1 / Invoice Furnishing Facility (IFF) and communicated to the recipient in Form GSTR-2B.

If an invoice is entered in the taxpayer's internal Purchase Register (ERP/Accounting system) but is missing or improperly reported by the vendor in GSTR-2B:
1. The taxpayer risks immediate GST demand notices, interest (Section 50), and penalties.
2. Ineligible ITC claims lead to cash flow disruptions and tax audit queries.
3. Conversely, invoices in GSTR-2B that are missing from the purchase register lead to missed credit claims and unclaimed tax deductions.

**GST Reconciler** is built to bridge this gap: providing an offline, private, high-speed, intelligent reconciliation platform that compares any two GST data streams (e.g. GSTR-2B vs Purchase Register, or GSTR-1 vs Sales Ledger) and classifies discrepancies down to individual penny differences and typographical invoice number mismatches.

---

## 2. Core Functional Requirements

### FR-01: Heterogeneous Ingestion
- Ingest Excel spreadsheets (.xlsx, .xls), CSVs, vector PDFs, scanned PDF vouchers, and image files.
- Automatically scan multi-sheet Excel workbooks and allow user selection or automatic sheet detection.
- Delimiter, encoding (UTF-8, Latin-1, CP1252), and header row detection.

### FR-02: Intelligent Auto Column Mapping
- Heuristic and pattern-based recognition for all canonical GST invoice attributes:
  - Supplier GSTIN / Buyer GSTIN
  - Legal / Trade Name
  - Invoice Number & Invoice Date
  - Invoice Type (Regular, Debit Note, Credit Note, SEZ, RCM)
  - Taxable Value
  - Integrated GST (IGST), Central GST (CGST), State/UT GST (SGST), and Cess
  - Total Invoice Value
  - Place of Supply (POS) state code
- Display match confidence percentage per field.
- Profile persistence: Save and reload mapping definitions for recurring ERP formats (Tally Prime, Busy, SAP, Zoho Books, Portal GSTR-2B).

### FR-03: Strict Data Normalization
- **GSTIN Normalization**: 15-character alphanumeric formatting, whitespace removal, uppercase casting, and modulo 36 check-digit verification.
- **Invoice Number Normalization**: Stripping leading zeros, special characters (`/`, `-`, `_`, space), case-folding, and preservation of raw string for audit verification.
- **Date Normalization**: Parsing multi-format dates (`DD/MM/YYYY`, `DD-MM-YYYY`, `YYYY-MM-DD`, `DD-Mon-YYYY`, Excel serial timestamps) to ISO standard `YYYY-MM-DD`.
- **Financial Precision**: Absolute `Decimal` floating-point handling, avoiding binary rounding issues.

### FR-04: Multi-Tier Reconciliation Engine
- **Level 1 (Exact Match)**: GSTIN + Raw Invoice Number + Date + Taxable & Tax values within tolerance.
- **Level 2 (Strong Match)**: GSTIN + Normalized Invoice Number + Values within tolerance.
- **Level 3 (Normalized Variation Match)**: GSTIN + Normalized Invoice Number with date variation within allowed tolerance window (e.g. ±30 days).
- **Level 4 (Fuzzy Match)**: Approximate invoice number match (e.g. typos, OCR character confusion `0`/`O`, `1`/`I`) or trade name similarity with strict confidence gating (>= 85%).

### FR-05: Configurable Tax Tolerances
- Independent tolerance thresholds for:
  - Taxable value (default: ₹5.00)
  - Tax components: IGST, CGST, SGST, Cess (default: ₹2.00)
  - Total invoice value (default: ₹5.00)
  - Date variation (default: 30 days)

### FR-06: Comprehensive Discrepancy Classification
- Exact categorization of mismatch reasons:
  - `MATCHED`: Identical within configured tolerances.
  - `MATCHED_WITH_DIFFERENCE`: Matched key, but amount differs beyond tolerance.
  - `MISSING_IN_SOURCE_A`: Present in Purchase Register but missing from GSTR-2B (ITC at Risk).
  - `MISSING_IN_SOURCE_B`: Present in GSTR-2B but missing from Purchase Register (Unclaimed ITC).
  - `DUPLICATE`: Repeated invoice instances within the same source dataset.
  - `INVALID_DATA`: Malformed GSTIN, invalid date, or negative invalid values.
  - Specific value mismatch tags: `TAXABLE_VALUE_MISMATCH`, `IGST_MISMATCH`, `CGST_MISMATCH`, `SGST_MISMATCH`, `DATE_MISMATCH`.

### FR-07: Interactive Executive Dashboard & Review
- High-level KPIs: Total Records, Matched Rate, Total Value at Risk, Unclaimed ITC, Duplicate Exposure.
- Side-by-side comparison screen for examining Source A vs Source B with visual color-coded difference indicators.
- Manual review workflow: Flag items as `ACCEPTED`, `REJECTED`, or `IGNORED`.

### FR-08: Audit-Ready Multi-Format Export
- Formatted Excel report (`.xlsx`) with stylized summary tab, discrepancy analysis tab, and raw record ledgers.
- CSV export for direct ERP re-import.

---

## 3. Non-Functional Requirements (NFR)

* **NFR-01: Performance**: Reconcile 50,000 records across two files in under 5 seconds.
* **NFR-02: Offline Privacy**: Zero outbound network requests during import, normalization, matching, review, and export.
* **NFR-03: Zero Technical Footprint**: Standalone single-click Windows `.exe` installer. No Python or external database dependencies required on target machine.
* **NFR-04: Resilience & ACID Storage**: Atomic transactions via local SQLite WAL mode; auto-backup before database migration.
