# Executive Dashboard Specification

## 1. Top Metric Cards

The top row of the dashboard presents four critical financial indicators:

```text
┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│ TOTAL PROCESSED      │ MATCHED RATE         │ ITC AT RISK          │ TAX DIFFERENCE       │
│ 12,450 Invoices      │ 11,280 (90.6%)       │ ₹ 3,42,850.00        │ ₹ 14,210.00          │
│ Source A: 6,100      │ Exact: 10,400        │ 410 Invoices missing │ In 180 matched       │
│ Source B: 6,350      │ Fuzzy: 880           │ in GSTR-2B           │ invoices             │
└──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

---

## 2. Discrepancy Breakdown Section

A structured status breakdown table and visual bar breakdown showing:
* **Matched within tolerance**: Counts and value
* **Taxable Value Mismatch**: Counts and net delta
* **Tax Component Mismatches (IGST / CGST / SGST)**: Counts and net delta
* **Missing in Portal (GSTR-2B)**: Counts and ITC amount
* **Missing in Books (Purchase Register)**: Counts and ITC amount
* **Duplicate Invoices**: Intra-source duplicate occurrences
