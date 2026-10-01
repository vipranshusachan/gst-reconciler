# Application Architecture

## 1. Application Layer Structure

The application layer coordinates interactions between user commands (GUI or CLI) and domain services.

### Core Components
* **`ReconciliationService`**: Orchestrates the multi-stage pipeline:
  1. Inspect source files and extract tabular schemas.
  2. Apply auto-mapping heuristics or user-selected mapping profiles.
  3. Validate and normalize raw records into canonical `InvoiceRecord` entities.
  4. Invoke `ReconciliationEngine` with user-configured tolerance parameters.
  5. Commit match results, differences, and audit log entries to the local SQLite database.
* **Worker Execution Architecture**:
  - `ReconciliationWorker(QThread)`: Background thread emitting Qt signals:
    - `progress_changed(int current, int total, str status_message)`
    - `reconciliation_completed(ReconciliationSummary summary)`
    - `reconciliation_failed(str error_message)`
  - Cancellation token support: Users can safely halt execution between processing phases without database corruption.

---

## 2. Desktop UI Component Architecture

The desktop UI uses PySide6 adhering to the Model-View-Presenter (MVP) / Model-View-Controller pattern:

```
┌────────────────────────────────────────────────────────┐
│                   MainWindow (View)                    │
│   ├── Navigation Bar (Dashboard, Reconcile, Issues...) │
│   └── Central QStackedWidget                           │
│       ├── DashboardView                                │
│       ├── ImportWizardView                             │
│       ├── IssueExplorerView                            │
│       ├── ComparisonModalView                          │
│       └── SettingsView                                 │
└───────────────────────────┬────────────────────────────┘
                            │ Signals / Slots
                            ▼
┌────────────────────────────────────────────────────────┐
│               Presenters / Controllers                 │
│   - Manage view state, table models, and user input    │
│   - Communicate with ReconciliationService             │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│             Virtual Table Models (Qt)                  │
│   - ReconciledTableModel (QAbstractTableModel)         │
│   - Lazy fetch, custom cell rendering & color badges   │
└────────────────────────────────────────────────────────┘
```
