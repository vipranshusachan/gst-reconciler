# Reconciliation Matching Engine

## 1. Multi-Stage Pipeline Architecture

The reconciliation engine operates in four progressive stages:

```
Pass 0: Intra-Source Deduplication
  │  - Flags duplicate invoices within Source A and Source B independently.
  ▼
Pass 1: Level 1 Exact Match
  │  - Key: (GSTIN, Raw Invoice No, Date)
  │  - Verifies amount differences against tolerance.
  ▼
Pass 2: Level 2 Strong Match
  │  - Residual unmatched pool.
  │  - Key: (GSTIN, Normalized Alphanumeric Invoice No)
  ▼
Pass 3: Level 3 Normalized Variation Match
  │  - Residual unmatched pool.
  │  - Key: (GSTIN, Core Numeric Token) + Date within tolerance window (±30 days).
  ▼
Pass 4: Level 4 Gated Fuzzy Match
  │  - Residual unmatched pool.
  │  - Match on same GSTIN + Levenshtein / Token Ratio $\ge$ 85% on invoice string,
  │    OR identical Taxable Amount + approximate supplier name.
  ▼
Pass 5: Discrepancy Classification & Missing Categorization
  │  - Remaining unmatched records in Source A -> `MISSING_IN_SOURCE_B`.
  │  - Remaining unmatched records in Source B -> `MISSING_IN_SOURCE_A`.
```

---

## 2. Independence from UI

The engine is completely decoupled from PySide6 and GUI widgets. It is encapsulated within `app.reconciliation.engine.ReconciliationEngine` and accepts pure Python domain collections:

```python
engine = ReconciliationEngine(tolerances=Tolerances(taxable=5.0, tax=2.0))
summary = engine.reconcile(records_a=source_a_invoices, records_b=source_b_invoices)
```
