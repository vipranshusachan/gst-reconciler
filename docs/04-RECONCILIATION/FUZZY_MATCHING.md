# Fuzzy Matching & Confidence Gating

## 1. Safety Principles for Fuzzy Matching

Fuzzy matching in accounting must never be permitted to silently match unrelated financial records. A false positive can result in wrongful ITC claims or improper vendor payments.

### Guardrails:
1. **Never match on fuzzy alone**: Fuzzy string matching is restricted to candidate pairs that already share an invariant anchor:
   - Same `supplier_gstin`, OR
   - Identical `taxable_value` and exact same invoice date.
2. **Explicit Confidence Gating**: Only candidate pairs achieving a composite score $\ge 85\%$ are considered.
3. **Transparent Match Reason**: All fuzzy matches are flagged with `match_level = FUZZY` and the exact calculated similarity score (e.g. `92%`).

---

## 2. Algorithms Employed

* **Token Sort Ratio**: Splits strings into whitespace/punctuation tokens, sorts them alphabetically, and joins them. This handles transposed invoice segments (e.g. `2026-INV-101` vs `INV-2026-101`).
* **Normalized Levenshtein Distance**: Computes minimal single-character edits (insertions, deletions, substitutions) divided by max string length. Catches standard OCR and typing mistakes (`INV001` vs `INV00I`).
