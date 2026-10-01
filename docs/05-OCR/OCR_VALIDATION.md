# OCR Validation & Error Correction

## 1. Common Optical Character Recognition Artifacts

Scanned accounting vouchers frequently suffer from character confusion:
* `0` (Zero) misread as `O` or `D`.
* `1` (One) misread as `I` or `l` (lowercase L) or `|` (pipe).
* `8` misread as `B`.
* `5` misread as `S`.

---

## 2. Validation & Repair Heuristics

1. **GSTIN Context-Aware Correction**:
   - The first two characters of a GSTIN are strictly digits (`[0-9]{2}`). If character 1 or 2 is parsed as `O`, it is repaired to `0`. If `I` or `l`, repaired to `1`.
   - Characters 3 to 7 are the PAN alphabetic code (`[A-Z]{5}`). Any digits in these positions are flagged for review.
   - Character 14 is always the character `Z`. If OCR parsed it as `2`, it is corrected to `Z`.
2. **Mathematical Balance Validation**:
   - Condition: $|(Taxable + IGST + CGST + SGST + Cess) - TotalValue| \le 1.00$.
   - If the sum of tax components and taxable base equals total invoice value within ₹1, confidence is scored high ($>95\%$). If unbalanced, confidence is reduced and user inspection is requested.
