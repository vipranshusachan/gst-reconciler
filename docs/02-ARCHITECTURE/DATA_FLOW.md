# Data Flow Architecture

The reconciliation pipeline transforms raw user files into actionable discrepancy audit ledgers via five distinct stages:

```
[Raw Files: Source A & Source B]
                │
                ▼ (Stage 1: Ingestion)
[Raw Tabular Records: List[Dict[str, Any]]]
                │
                ▼ (Stage 2: Column Mapping & Extraction)
[Extracted Raw Invoice Dictionaries]
                │
                ▼ (Stage 3: Normalization & Validation)
[Canonical InvoiceRecord Entities (Pydantic / Dataclasses)]
                │
                ▼ (Stage 4: Reconciliation Engine)
    ├── Deduplication Pass (Identify intra-source repeats)
    ├── Level 1: Exact Hash Matching (GSTIN + InvNo + Date + Amounts)
    ├── Level 2: Strong Normalized Matching (GSTIN + CleanInvNo + Amounts)
    ├── Level 3: Date-Window Matching (CleanInvNo + Date Window)
    └── Level 4: Selective Gated Fuzzy Matching (Levenshtein >= 85%)
                │
                ▼ (Stage 5: Difference & Classification)
[MatchRecord Entities with Granular Discrepancy Taxonomy]
                │
        ┌───────┴───────────────────────┐
        ▼                               ▼
[SQLite Storage & Session]      [UI Dashboard & Exporters]
```

### Stage Transformations:
1. **Ingestion**: Raw bytes -> Stream of string cells.
2. **Mapping**: Raw header names -> Canonical field keys (`supplier_gstin`, `invoice_number`, `taxable_value`, etc.).
3. **Normalization**:
   - `supplier_gstin`: Stripped of whitespace, uppercase, checksum verified.
   - `invoice_number`: Leading zeros removed, special separators normalized into clean alphanumeric tokens.
   - `amounts`: Converted from string/float to `Decimal` rounded to two decimal places.
4. **Reconciliation**: Grouped into hash buckets by `(gstin, normalized_invoice_no)`. Unmatched items pass down through fallback stages.
5. **Classification**: Mismatches receive exact numeric difference deltas (`diff_taxable`, `diff_igst`, `diff_cgst`, `diff_sgst`, `diff_cess`, `diff_total`) and a human-readable diagnosis string.
