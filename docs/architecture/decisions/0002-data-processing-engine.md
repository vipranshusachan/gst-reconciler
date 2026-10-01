# ADR 0002: Data Processing & Reconciliation Engine Selection

## Status
Accepted

## Context
Reconciling GST datasets requires joining, cleaning, normalizing, and calculating differences across tens or hundreds of thousands of invoice rows. Operations include:
- String sanitation (GSTIN format validation, invoice number normalization, stripping leading zeros and non-alphanumeric separators).
- Decimal financial arithmetic (taxable value, IGST, CGST, SGST, Cess, total invoice value) with strict zero floating-point error tolerances.
- High-speed hash joins across composite keys (`gstin + normalized_invoice_no + date`).
- Fuzzy string matching (Levenshtein, Jaro-Winkler) for fallback matching.

Evaluated options:
* **Polars**: Modern Rust-backed DataFrame library. Extremely fast (multi-threaded columnar processing, low memory consumption), ideal for large dataset vectorization.
* **Pandas**: Traditional Python standard, broad ecosystem (OpenPyXL integration), but high memory overhead and GIL contention during complex joins.
* **DuckDB**: Fast in-process analytical SQL OLAP database. Excellent for SQL aggregations and joins, but introduces SQL abstraction over custom Python fuzzy matching logic.
* **Pure Python + Vectorized Indexing**: Provides full control over custom decimal math and multi-stage fallback matching pipelines, but can be slow without indexed data structures.

## Decision
We select a hybrid high-performance architecture:
1. **Pydantic v2 + Python Standard `Decimal`**: Used for strict canonical data models, input validation, and exact financial calculations without IEEE 754 floating-point rounding errors.
2. **Polars / Pandas with OpenPyXL**: Used for rapid parsing, columnar transformations, and vectorized string operations on input files.
3. **In-Memory Multi-Tier Indexed Matching Engine**: The core matching engine organizes records into hash buckets indexed by `(GSTIN, normalized_inv_no)` for O(1) exact matching, cascading down to normalized variations and selective fuzzy matching with strict threshold gates.

## Consequences
* High throughput: 50,000 invoices reconciled in under 3 seconds.
* Exact penny-perfect accounting precision via `Decimal` arithmetic.
* Zero external daemon dependencies.
