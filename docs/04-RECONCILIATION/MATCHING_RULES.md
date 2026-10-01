# Matching Rules Specification

## 1. Level 1: Exact Match Rule
* **Conditions**:
  1. `supplier_gstin_A == supplier_gstin_B`
  2. `raw_invoice_number_A.strip() == raw_invoice_number_B.strip()`
  3. `invoice_date_A == invoice_date_B` (or one is absent)
* **Amount Verification**:
  - $|taxable_A - taxable_B| \le tolerance.taxable$
  - $|tax_A - tax_B| \le tolerance.tax$
* **Result**:
  - If amounts pass: `MATCHED` (Level: `EXACT`, Score: 1.0)
  - If amounts fail: `MATCHED_WITH_DIFFERENCE` (Level: `EXACT`, Score: 1.0)

---

## 2. Level 2: Strong Normalized Match Rule
* **Conditions**:
  1. `supplier_gstin_A == supplier_gstin_B`
  2. `clean(invoice_number_A) == clean(invoice_number_B)`
     (where `clean` strips leading zeros and non-alphanumeric characters, e.g. `INV/0042` matches `INV-42`)
* **Result**:
  - `MATCHED` or `MATCHED_WITH_DIFFERENCE` (Level: `STRONG`, Score: 0.95)

---

## 3. Level 3: Normalized Variation Match Rule
* **Conditions**:
  1. `supplier_gstin_A == supplier_gstin_B`
  2. Core numeric token matches (e.g. `42` in `DEL/42/26` vs `42/26`)
  3. $|date_A - date_B| \le tolerance.date\_days$ (e.g. 30 days)
* **Result**:
  - `MATCHED` or `MATCHED_WITH_DIFFERENCE` (Level: `NORMALIZED`, Score: 0.90)
