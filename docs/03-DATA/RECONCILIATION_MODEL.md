# Reconciliation Data Model & States

## 1. Match Status Taxonomy

Every comparison outcome is categorized into one of five primary states:

```
                  ┌──────────────────────┐
                  │ Reconciliation Item  │
                  └──────────┬───────────┘
                             │
     ┌───────────────────────┼────────────────────────┐
     ▼                       ▼                        ▼
┌─────────┐      ┌────────────────────────┐      ┌─────────┐
│ MATCHED │      │ MATCHED_WITH_DIFF      │      │ MISSING │
└─────────┘      └────────────────────────┘      └────┬────┘
                                                      │
                                          ┌───────────┴───────────┐
                                          ▼                       ▼
                                  ┌───────────────┐       ┌───────────────┐
                                  │ MISSING_IN_A  │       │ MISSING_IN_B  │
                                  └───────────────┘       └───────────────┘
```

1. **`MATCHED`**: Records from Source A and Source B match across composite keys and all monetary amounts fall strictly within user-configured tolerances.
2. **`MATCHED_WITH_DIFFERENCE`**: Records match on key identity (e.g. GSTIN + Invoice Number), but financial amounts (Taxable, IGST, CGST, SGST, Cess, or Total) differ beyond allowed tolerance.
3. **`MISSING_IN_SOURCE_A`**: Invoice exists in Source B (e.g. Purchase Register) but cannot be found in Source A (GSTR-2B). This indicates **Input Tax Credit at Risk**.
4. **`MISSING_IN_SOURCE_B`**: Invoice exists in Source A (GSTR-2B) but is absent from Source B (Purchase Register). This represents **Unclaimed / Missed ITC**.
5. **`DUPLICATE`**: Repeated occurrence of the same GSTIN and invoice number within the same source dataset.

---

## 2. Match Levels

The engine records the specific level through which a match was established:
* **`EXACT` (Level 1)**: Exact GSTIN, raw invoice number, date, and amounts.
* **`STRONG` (Level 2)**: Exact GSTIN and normalized invoice number.
* **`NORMALIZED` (Level 3)**: Normalized invoice number with date within permitted window.
* **`FUZZY` (Level 4)**: Approximate string match meeting confidence threshold ($\ge 85\%$).
