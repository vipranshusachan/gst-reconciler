# Security Architecture

## 1. Threat Modeling & Local Privacy Boundary

Tax data contains sensitive corporate financial secrets (turnover, customer pricing, supplier networks, PAN/GSTIN identifiers). GST Reconciler is engineered with an uncompromising security posture:

### Security Guarantees
1. **Air-Gapped Operation**: The entire core engine runs without internet connectivity. Outbound sockets are never opened during parsing, reconciliation, database writes, or report generation.
2. **Local Data Isolation**:
   - Application data resides strictly in `%APPDATA%\GSTReconciler\data.db`.
   - File permissions on the SQLite database and log directories inherit user-level access controls (ACLs) on Windows.
3. **No Dynamic Code Execution**: Ingestion parsers (Excel, CSV, PDF) use safe streaming readers. Macro execution in `.xlsm` files is disabled.
4. **Structured Logging Privacy**: Application logs (`logs/app.log`) capture operational events and error stacks, but explicitly mask sensitive identifiers (e.g. GSTIN masked to `27******1Z5`, amounts stripped from debug messages).

---

## 2. STRIDE Threat Assessment

| Threat Category | Potential Attack Vector | Mitigation in GST Reconciler |
|---|---|---|
| **Spoofing** | Malicious fake update package | Update releases must be manually accepted; executable checksums (SHA-256) verified. |
| **Tampering** | In-flight database corruption | SQLite Write-Ahead Logging (WAL) ensures atomic ACID transaction commits. |
| **Repudiation** | User denies manual override | Full local audit log records timestamp and reason for all user decisions. |
| **Information Disclosure** | Leak of vendor GST data | 100% offline-first; no remote analytics or error reporting beacons. |
| **Denial of Service** | Decompression bomb / huge Excel | Streaming parsing with row limits and worker thread cancellation checkpoints. |
| **Elevation of Privilege** | Executable hijacking | Windows installer installs to user `%LOCALAPPDATA%` or standard `Program Files` with proper permissions. |
