# Security Policy

## 🔒 Security & Privacy Guarantees

GST Reconciler is built on a strict **Offline-First & Local-Only** architecture:
1. **Zero External Telemetry**: The application never transmits invoice records, GSTINs, financial metrics, or user telemetry to any remote server.
2. **Local Storage**: All data, projects, mapping profiles, and match ledgers are persisted in a local SQLite database in the user's local operating system directory.
3. **Data Integrity**: Imported files are read-only. Original files are never modified in place.
4. **No Mandatory Network Connection**: The core application functions 100% disconnected from the internet. Optional internet checks are limited to user-initiated GitHub release version checks.

---

## 🛡️ Supported Versions

| Version | Supported |
|---|---|
| 1.0.x | :white_check_mark: |
| < 1.0 | :x: |

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability in GST Reconciler:

1. **DO NOT file a public GitHub issue.** Public issues must never contain potential exploits or sensitive logs.
2. Email your findings directly to the security team at: `security@gstreconciler.local` or contact the core maintainers via GitHub Security Advisories.
3. Include:
   - Detailed description of the vulnerability.
   - Minimal reproducible test script or scenario (using synthetic mock data only).
   - Any potential impact on local data integrity or code execution.
4. The maintainers will respond within 48 hours to acknowledge receipt and coordinate a patch.
