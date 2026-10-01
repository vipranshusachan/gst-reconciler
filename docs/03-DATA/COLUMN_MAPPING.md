# Smart Column Mapping Engine

## 1. Heuristic Detection Strategy

The column mapping engine analyzes imported tabular headers using regular expressions and semantic synonym weights.

### Mapping Dictionary & Patterns

| Canonical Field | Synonyms / Patterns Detected |
|---|---|
| `supplier_gstin` | `gstin`, `gstin_uin`, `gst_no`, `supplier_gstin`, `vendor_gstin`, `tin_no`, `gstin of supplier` |
| `supplier_name` | `supplier_name`, `party_name`, `vendor_name`, `trade_name`, `legal_name`, `name of supplier`, `party` |
| `invoice_number` | `invoice_number`, `invoice_no`, `inv_no`, `bill_no`, `doc_no`, `document_number`, `voucher_no`, `inv no.` |
| `invoice_date` | `invoice_date`, `inv_date`, `bill_date`, `doc_date`, `date`, `voucher_date` |
| `taxable_value` | `taxable_value`, `taxable_amount`, `taxable_amt`, `taxable`, `assessable_value`, `base_amount` |
| `igst` | `igst`, `igst_amount`, `integrated_tax`, `igst_amt`, `integrated_gst` |
| `cgst` | `cgst`, `cgst_amount`, `central_tax`, `cgst_amt`, `central_gst` |
| `sgst` | `sgst`, `sgst_amount`, `state_tax`, `sgst_amt`, `utgst`, `state_gst` |
| `cess` | `cess`, `cess_amount`, `compensation_cess`, `cess_amt` |
| `total_invoice_value` | `total_amount`, `invoice_value`, `inv_value`, `total_invoice_value`, `gross_total`, `bill_amount`, `total` |
| `place_of_supply` | `place_of_supply`, `pos`, `state_code`, `supply_place` |

---

## 2. Confidence Scoring Algorithm

The detection algorithm computes a confidence score (0% to 100%):
- **Exact Keyword Match**: 100%
- **Normalized Substring Match**: 85% - 95%
- **Fuzzy Token Similarity Match**: 70% - 84%
- **Data Content Sampling Inspection**: If a column header is ambiguous, the mapper samples the first 10 data rows. For instance, if 90% of rows match the 15-character GSTIN regex `^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$`, confidence in `supplier_gstin` increases to 99%.

---

## 3. Mapping Profiles

Users can save mapping configurations as reusable profiles stored in SQLite:
* `Profile: Tally Prime Purchase Register`
* `Profile: Busy 21 Purchase List`
* `Profile: Portal Official GSTR-2B Excel`
* `Profile: Zoho Books Bill Export`
* `Profile: SAP B1 Journal Voucher`
