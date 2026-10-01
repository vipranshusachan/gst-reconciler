# User Journeys

## Journey 1: Standard Monthly Reconciliation (GSTR-2B vs Purchase Register)

```
[Start]
  │
  ▼
1. Launch GST Reconciler Desktop Application
  │
  ▼
2. Click "New Reconciliation" on Dashboard
  │
  ▼
3. Select Source Files (Drag & Drop or File Browser):
   - Source A: "GSTR-2B_27AABCT3518Q1Z6_September_2026.xlsx" (Portal Return)
   - Source B: "Tally_Purchase_Register_Sep2026.xlsx" (ERP Books)
  │
  ▼
4. Inspect Auto-Detected Sheet Names & Headers
   - System previews the first 5 rows of each sheet.
  │
  ▼
5. Column Mapping Step:
   - System auto-maps headers with confidence scores (e.g., "Supplier GSTIN" -> 99%).
   - User reviews mappings and confirms or overrides any unmapped column.
   - User clicks "Save as Mapping Profile" (e.g., "Tally Prime Purchase").
  │
  ▼
6. Set Tolerances:
   - Amount Tolerance: ₹5.00
   - Date Tolerance: 30 days
   - Fuzzy Matching: Enabled (Threshold: 85%)
  │
  ▼
7. Click "Run Reconciliation"
   - Worker thread processes records; progress bar updates in real-time.
  │
  ▼
8. View Executive Dashboard:
   - Summary cards: 4,820 Records Total | 4,510 Matched (93.5%) | 310 Issues.
   - ITC at Risk: ₹2,45,600 (Missing in GSTR-2B).
  │
  ▼
9. Review Exceptions:
   - User switches to "Issue Explorer".
   - Filters by "Missing in 2B" or "Tax Differences".
   - Double-clicks an issue to view side-by-side comparison modal.
   - Flags 5 entries as "Accepted" (allowable differences).
  │
  ▼
10. Export Final Audit Report:
    - User clicks "Export to Excel".
    - System produces a clean multi-tab `.xlsx` file ready for vendor follow-up.
  │
  ▼
[Complete]
```
