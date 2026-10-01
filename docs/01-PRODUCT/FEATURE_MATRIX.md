# Feature Matrix

| Feature Domain | Feature Item | Capability / Specification | Status |
|---|---|---|---|
| **Ingestion** | Excel (.xlsx, .xls) | Multi-sheet detection, header detection, blank row stripping | Complete |
| **Ingestion** | CSV / TSV | Auto delimiter detection (`,`, `;`, `\t`, `\|`), encoding auto-detect | Complete |
| **Ingestion** | PDF Vector Text | Direct text parsing, table boundary extraction | Complete |
| **Ingestion** | OCR Engine | Modular provider abstraction (Tesseract, PDFPlumber) | Complete |
| **Mapping** | Smart Detection | Regex + semantic keyword dictionary for Indian GST headers | Complete |
| **Mapping** | Profiles | Save, load, and auto-suggest mapping profiles | Complete |
| **Normalization** | GSTIN Sanitizer | Upper case, whitespace strip, 15-char regex & checksum validation | Complete |
| **Normalization** | Invoice Cleanse | Strip leading zeros, normalize special delimiters (`/`, `-`, `_`) | Complete |
| **Normalization** | Date Standard | Parse multi-format dates to ISO `YYYY-MM-DD` | Complete |
| **Matching** | Level 1: Exact | GSTIN + Raw Invoice No + Date + Exact amounts within tolerance | Complete |
| **Matching** | Level 2: Strong | GSTIN + Normalized Invoice No + Exact amounts within tolerance | Complete |
| **Matching** | Level 3: Normalized | Normalized Invoice No + Date within configured window (e.g. 30 days) | Complete |
| **Matching** | Level 4: Fuzzy | Levenshtein / Token similarity on invoice numbers and trade names | Complete |
| **Matching** | Duplicate Filter | Duplicate identification across GSTIN + Invoice Number per source | Complete |
| **Matching** | Difference Logic | Configurable tolerances (₹1–₹10) for Taxable, IGST, CGST, SGST, Cess | Complete |
| **Classification** | Discrepancies | 16+ granular discrepancy categories with human explanation | Complete |
| **UI & UX** | Dashboard | Summary KPIs, ITC at risk, discrepancy distribution charts | Complete |
| **UI & UX** | Issue Explorer | Virtualized table, multi-column search, type filtering, pagination | Complete |
| **UI & UX** | Side-by-Side | Dual view of Source A vs Source B with visual difference color tags | Complete |
| **UI & UX** | Review Flow | Action buttons: Reviewed, Accepted, Rejected, Ignored | Complete |
| **Persistence** | SQLite WAL | Embedded local database, automatic schema migrations, backup | Complete |
| **Export** | Excel Report | Multi-sheet formatted workbook with styles, filters, and summaries | Complete |
| **Export** | CSV Report | Comma-separated value export of reconciled ledger | Complete |
| **CLI** | Headless Runner | `gst-reconciler reconcile ...` command line interface | Complete |
| **Packaging** | Windows EXE | PyInstaller standalone bundle + Inno Setup installer | Complete |
