# Mismatch Classification Taxonomy

When records fail exact matching or exhibit discrepancies, the classification engine assigns granular, human-readable issue tags:

| Category Code | Description | Statutory Impact |
|---|---|---|
| `MATCHED` | Full match across key and monetary attributes within tolerance | Safe to claim in GSTR-3B |
| `MATCHED_WITH_DIFFERENCE` | Matching invoice with amount differences exceeding tolerance | Tax difference needs adjustment |
| `MISSING_IN_SOURCE_A` | Present in Purchase Register, absent in GSTR-2B | **ITC at Risk** (Supplier failed to file GSTR-1) |
| `MISSING_IN_SOURCE_B` | Present in GSTR-2B, absent in Purchase Register | **Unclaimed ITC** (Invoice not booked in ERP) |
| `DUPLICATE` | Repeated invoice under same GSTIN in the same source | Risk of duplicate payment or excess claim |
| `TAXABLE_VALUE_MISMATCH` | Base taxable amount differs between sources | Assessable value mismatch |
| `IGST_MISMATCH` | Integrated GST differs | Potential Place of Supply misclassification |
| `CGST_MISMATCH` | Central GST differs | Rate difference |
| `SGST_MISMATCH` | State/UT GST differs | Rate difference |
| `CESS_MISMATCH` | Compensation Cess differs | Cess calculation mismatch |
| `DATE_MISMATCH` | Invoice dates differ beyond date window tolerance | Timing difference / accounting period lag |
| `INVALID_GSTIN` | GSTIN fails 15-character statutory checksum | Invalid tax invoice under GST rules |
| `LOW_CONFIDENCE_MATCH` | Fuzzy match candidate between 85% and 90% | Requires manual verification by accountant |
