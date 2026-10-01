# UX Flows & User Interaction

## 1. Import & Reconciliation Wizard Flow

```text
[Step 1: Choose Files]
  - Drag and drop or browse Source A (e.g. GSTR-2B) and Source B (Purchase Register).
  - Select active sheets if multi-sheet Excel files.
  - Click "Next: Map Columns".

[Step 2: Column Mapping & Verification]
  - Table of canonical fields vs source columns.
  - Auto-mapped fields highlighted with confidence chips (e.g. "99% Confirmed").
  - Dropdown selectors allow manual column overrides.
  - Option to "Save Mapping Profile".
  - Click "Next: Tolerances".

[Step 3: Tolerances & Rules]
  - Set Taxable tolerance (default ₹5.00) and Tax component tolerance (default ₹2.00).
  - Toggle Fuzzy Matching checkbox.
  - Click "Run Reconciliation".

[Step 4: Real-time Progress & Completion]
  - Progress bar with percentage and step description.
  - Auto-transitions to Dashboard upon completion.
```

---

## 2. Issue Resolution & Manual Review Flow

1. In the **Issue Explorer**, the user selects a row and clicks **Inspect (Side-by-Side)**.
2. A comparison dialog renders Source A values on the left and Source B values on the right. Differences in amounts are highlighted with amber warning badges.
3. The user can change the Review Status:
   - **Accepted**: Mark discrepancy as an approved round-off or timing adjustment.
   - **Rejected**: Mark as a vendor error requiring vendor debit note.
   - **Ignored**: Disregard for statutory filing purposes.
4. The review status is saved in SQLite and reflected on the export report.
