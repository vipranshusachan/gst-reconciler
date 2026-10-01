# Test Cases Matrix

| Test Suite | Test ID | Description | Expected Outcome |
|---|---|---|---|
| **Normalization** | `TC-NORM-01` | Valid GSTIN format (`27AABCT3518Q1Z6`) | `is_valid == True`, formatted uppercase |
| **Normalization** | `TC-NORM-02` | Invalid GSTIN format (length 14, invalid regex) | `is_valid == False`, validation error recorded |
| **Normalization** | `TC-NORM-03` | Invoice number trimming (`  inv/0042-b  `) | Normalized to `INV/42-B` |
| **Normalization** | `TC-NORM-04` | Date parsing (`15/09/2026`, `2026-09-15`, `15-Sep-2026`) | All resolve to `date(2026, 9, 15)` |
| **Matching** | `TC-MATCH-01` | Exact match Level 1 with ₹0 difference | Status: `MATCHED`, Level: `EXACT`, Score: 1.0 |
| **Matching** | `TC-MATCH-02` | Amount difference within ₹2 tolerance | Status: `MATCHED`, Level: `EXACT` |
| **Matching** | `TC-MATCH-03` | Amount difference exceeding tolerance (₹50 diff) | Status: `MATCHED_WITH_DIFFERENCE` |
| **Matching** | `TC-MATCH-04` | Normalized invoice match (`INV/042` vs `INV-42`) | Status: `MATCHED`, Level: `STRONG` |
| **Matching** | `TC-MATCH-05` | Typo in invoice number (`INV-1092` vs `INV-109Z`) | Status: `MATCHED` or flagged, Level: `FUZZY` (Score > 0.85) |
| **Matching** | `TC-MATCH-06` | Invoice present in B but missing in A | Status: `MISSING_IN_SOURCE_A` |
| **Matching** | `TC-MATCH-07` | Intra-source duplicate invoice numbers | Status: `DUPLICATE` |
| **Ingestion** | `TC-ING-01` | Excel file with blank header rows | Correct header row detected; data imported cleanly |
| **Ingestion** | `TC-ING-02` | CSV with semicolon delimiter and Latin-1 encoding | Delimiter and encoding auto-detected |
| **Export** | `TC-EXP-01` | Excel export generation | Formatted `.xlsx` file written with proper summary and tabs |
