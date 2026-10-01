# Data Normalization Engine

## 1. Principles of Immutability

Raw user data is sacred. The normalization layer produces standardized values for high-speed indexing and matching, but **never overwrites or destroys the original raw imported strings**. Both values are maintained side-by-side in `InvoiceRecord.raw_invoice_number` and `InvoiceRecord.invoice_number`.

---

## 2. GSTIN Normalization

The Goods and Services Tax Identification Number (GSTIN) is a 15-character alphanumeric identifier formatted as:
`[State Code (2)][PAN (10)][Entity No (1)][Z (1)][Check Digit (1)]`

### Normalization Steps:
1. Strip all leading, trailing, and embedded spaces, dashes, or tabs.
2. Convert all characters to uppercase.
3. Validate format against statutory regex:
   `^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$`
4. If format fails or length $\neq 15$, flag `is_valid_gstin = False` and record a validation error.

---

## 3. Invoice Number Normalization

Different ERPs and accountants format identical invoice numbers differently:
- Source A: `INV/2026-27/0042`
- Source B: `inv-2026-27-42`
- Scanned PDF: `INV 2026 27 0042`

### Normalization Pipeline:
1. **Case-Folding**: Convert to uppercase.
2. **Whitespace Stripping**: Remove all space characters.
3. **Delimiter Cleaning**: Normalize `/`, `-`, `_`, `.` to a uniform delimiter or strip non-alphanumeric characters for clean indexing.
4. **Leading Zero Removal**: Strip non-significant leading zeros in numeric sequences (e.g., `0042` -> `42`).

---

## 4. Date Normalization

Dates arrive in multiple representations across ERPs:
- Text dates: `15/09/2026`, `15-09-2026`, `2026-09-15`, `15-Sep-2026`, `15.09.2026`
- Excel serial day numbers: e.g. `46280`

The date parser resolves all inputs into an ISO `datetime.date(YYYY, MM, DD)` instance.
