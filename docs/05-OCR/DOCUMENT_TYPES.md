# GST Document Types

The application handles standard Indian GST transaction document types:

| Document Type | Code | Ingestion Behavior |
|---|---|---|
| **B2B Tax Invoice** | `B2B` | Standard procurement voucher with taxable, CGST, SGST, IGST components. |
| **Credit Note** | `CDNR` | Value adjustment reducing ITC. Financial amounts are normalized as negative or explicit reductions. |
| **Debit Note** | `DBNR` | Value adjustment increasing ITC. |
| **SEZ with Payment** | `SEZWP` | Inter-state supply to SEZ units with IGST payment. |
| **SEZ without Payment** | `SEZWOP` | Zero-rated supply to SEZ without tax payment under LUT/Bond. |
| **Reverse Charge** | `RCM` | Inward supplies attracting reverse charge tax payable by recipient. |
| **Bill of Entry (Import)**| `IMPG` | Custom imports with IGST paid at port. |
