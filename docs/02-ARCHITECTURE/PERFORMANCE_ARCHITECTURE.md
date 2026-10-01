# Performance Architecture

## 1. Benchmarking Targets & Scalability Requirements

GST reconciliation at mid-sized and large enterprises often involves:
- 10,000 to 100,000+ purchase invoices per financial year.
- Millions of data points across multiple tax slabs.

### Performance SLA Targets:
* **10,000 Invoices**: Reconciled and indexed in < 1.0 second.
* **50,000 Invoices**: Reconciled and indexed in < 4.0 seconds.
* **100,000 Invoices**: Reconciled and indexed in < 9.0 seconds.
* **GUI Render Time**: Under 100ms for virtualized table pagination, regardless of dataset size.
* **Peak Memory Usage**: Under 350 MB RAM for 100k records.

---

## 2. Architectural Optimizations

1. **Hash Indexing vs Nested Loops**:
   - Naive matching algorithms compare every row in Source A against every row in Source B ($O(N \times M)$ complexity, resulting in $10^9$ operations for 50,000 rows).
   - GST Reconciler groups records by composite hash keys (`gstin`, `clean_invoice_no`), reducing exact and strong matching to $O(N + M)$ average time complexity.
2. **Selective Gated Fuzzy Matching**:
   - Fuzzy string matching (Levenshtein distance) is computationally expensive.
   - GST Reconciler only triggers fuzzy matching on the residual pool of unmatched records where the supplier GSTIN matches, or where taxable amounts match exactly within a narrow candidate bucket. This eliminates quadratic fuzzy matrix calculations.
3. **Virtualized Qt Table Models**:
   - GUI displays results using `QTableView` backed by a custom `QAbstractTableModel`.
   - Only visible rows (typically 30-50 rows in the viewport) are rendered into UI memory, preventing UI freezing.
4. **Streaming Ingestion**:
   - Excel and CSV parsers use streaming read modes (`read_only=True` in OpenPyXL), avoiding building massive DOM trees in Python memory.
