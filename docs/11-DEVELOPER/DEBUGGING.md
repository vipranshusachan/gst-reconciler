# Debugging Guide

## 1. Enabling Verbose Debug Logs

By default, the application writes `INFO` level logs to `logs/app.log`. To enable verbose diagnostic tracing:

```bash
# Set environment variable
set GST_RECONCILER_LOG_LEVEL=DEBUG

# Run application
gst-reconciler gui
```

---

## 2. Inspecting Local SQLite Database

The local database can be inspected with any standard SQLite viewer (e.g. SQLiteStudio, DB Browser for SQLite):

```bash
# Path to local database on Windows:
%APPDATA%\GSTReconciler\data.db
```

Key tables to inspect:
* `projects`: Saved reconciliation sessions.
* `mapping_profiles`: Reusable column definitions.
* `reconciliation_runs`: Run execution metadata.
* `matches`: Reconciled records with discrepancy codes.
