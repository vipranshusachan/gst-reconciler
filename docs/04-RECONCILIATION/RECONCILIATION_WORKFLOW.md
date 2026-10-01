# Reconciliation Execution Workflow

## Worker Thread Execution Model

To prevent UI latency or freezing during long reconciliation tasks, the engine executes asynchronously on a background worker thread (`QThread` in PySide6).

```
[UI Trigger: "Run Reconciliation"]
              │
              ▼
    [Spawn Worker Thread]
              │
              ├─► [Phase 1: Ingest & Parse Source A & B]
              │   └─► Emit `progress_changed(10%, "Parsing files...")`
              │
              ├─► [Phase 2: Normalize & Validate Data]
              │   └─► Emit `progress_changed(30%, "Validating GSTINs and dates...")`
              │
              ├─► [Phase 3: Intra-Source Deduplication]
              │   └─► Emit `progress_changed(45%, "Checking for duplicates...")`
              │
              ├─► [Phase 4: Multi-Tier Reconciliation Matching]
              │   ├─► Level 1 Exact Matching
              │   ├─► Level 2 Strong Matching
              │   ├─► Level 3 Normalized Variation Matching
              │   └─► Level 4 Gated Fuzzy Matching
              │   └─► Emit `progress_changed(75%, "Reconciling records...")`
              │
              ├─► [Phase 5: Persist Results to SQLite]
              │   └─► Emit `progress_changed(90%, "Saving audit ledger...")`
              │
              └─► [Phase 6: Emit Completion Signal]
                  └─► UI receives `reconciliation_completed(summary)`
                  └─► Switch UI View to Dashboard
```
