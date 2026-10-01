# Threat Model (STRIDE)

## 1. System Asset Identification

1. **User Financial Files**: Invoices, purchase registers, GSTR-2B spreadsheets.
2. **Local Application Database**: SQLite database storing projects and match history.
3. **Application Binaries**: `GSTReconciler.exe` and associated DLLs.

---

## 2. Threat Analysis & Mitigations

* **Tampering**: An external malicious process attempts to alter `data.db`.
  * *Mitigation*: Windows filesystem permissions protect the user's `%APPDATA%` directory; SQLite WAL checkpoints ensure transaction consistency.
* **Information Disclosure**: Unauthorized users reading logs containing financial data.
  * *Mitigation*: Logging sanitizes GSTINs and strips monetary values from INFO and DEBUG logs.
* **Denial of Service**: Corrupt or malformed Excel spreadsheets causing buffer overflow or unbounded memory consumption.
  * *Mitigation*: Streaming OpenPyXL parser with row size sanity checks and try-except error boundaries preventing crash propagation.
