# Reconciliation Test Data Generation

## 1. Synthetic Golden Dataset Design

To validate all matching levels and edge cases deterministically, we provide a synthetic data generator script (`tests/fixtures/generate_demo_data.py`).

### Scenario Breakdown in Demo Dataset:
1. **Perfect Matches (50 records)**: Exact same GSTIN, Invoice No, Date, and Amounts in both files.
2. **Round-Off Difference Matches (15 records)**: Identical keys, but Taxable and Tax amounts differ by ₹0.50 to ₹2.00 (within default tolerance).
3. **Significant Mismatches (10 records)**: Matching invoice numbers, but values differ by ₹50 to ₹1,500 (classified as `MATCHED_WITH_DIFFERENCE`).
4. **Normalized Formatting Variations (15 records)**:
   - Source A has `INV/2026/042`, Source B has `INV-2026-42`.
   - Source A has `BILL-0091`, Source B has `BILL 91`.
5. **Minor Typos / OCR Confusion (10 records)**:
   - Character substitution (`INV-8801` vs `INV-B801`).
6. **Missing in GSTR-2B (15 records)**: Invoices present in Purchase Register only (**ITC at Risk**).
7. **Missing in Purchase Register (10 records)**: Invoices present in GSTR-2B only (**Unclaimed ITC**).
8. **Intra-Source Duplicates (5 pairs)**: Invoices repeated in Purchase Register.
