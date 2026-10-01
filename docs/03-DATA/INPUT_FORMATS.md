# Input Formats Specification

GST Reconciler supports diverse accounting export formats and handles real-world structural inconsistencies.

## 1. Supported File Extensions & MIME Types

| Extension | Parser Engine | Features Supported |
|---|---|---|
| `.xlsx` | OpenPyXL | Multi-sheet scanning, header discovery, formula result evaluation |
| `.xls` | xlrd / OpenPyXL | Legacy Excel format support |
| `.csv`, `.tsv` | Standard Python / Polars | Delimiter sniffing (`,`, `;`, `\t`, `\|`), encoding detection (UTF-8, Latin-1, CP1252) |
| `.pdf` | PDFPlumber | Text extraction from digital vector PDFs, table boundary recognition |
| `.png`, `.jpg`, `.jpeg` | Tesseract OCR Provider | Image deskew, binarization, field coordinate regex extraction |

---

## 2. Inconsistency Tolerances Handled by Ingestion

1. **Floating Header Rows**: Files where headers do not start at Row 1 (e.g. accounting reports with 4 title banner rows). The parser scans down until it encounters recognizable GST header keywords.
2. **Merged Cells**: Spreadsheets with merged supplier name or GSTIN headers spanning multiple sub-columns.
3. **Blank / Summary Rows**: Automatic omission of blank spacer lines and trailing "Total" or "Grand Total" summary rows.
4. **Number Formatting**: Handling of commas in Indian currency notation (e.g. `₹ 1,50,000.00` or `150000.00 CR`), parentheses representing negative values `(150.00)`, and empty cells defaulting to `0.00`.
