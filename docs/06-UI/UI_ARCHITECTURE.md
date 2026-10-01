# Desktop UI Architecture

## 1. PySide6 (Qt for Python) Structure

The desktop interface uses PySide6 with a clean component hierarchy:

```
MainWindow
├── QWidget (Sidebar Navigation)
│   ├── Logo & Brand Title
│   ├── Navigation QListWidget / Buttons:
│   │   ├── Dashboard
│   │   ├── Reconcile (Wizard)
│   │   ├── Issue Explorer
│   │   ├── Reports & Export
│   │   ├── Settings
│   │   └── About
│   └── Version Tag
│
└── QStackedWidget (Central Content Area)
    ├── DashboardView
    ├── ImportWizardView
    ├── IssueExplorerView
    ├── ReportsView
    └── SettingsView
```

---

## 2. Model-View Pattern & Virtualization

All high-density tables use `QTableView` connected to subclasses of `QAbstractTableModel`:
* **`ReconciledTableModel`**: Virtualized table model wrapping the reconciliation result dataset.
* **Instant Filtering**: Uses `QSortFilterProxyModel` or in-memory sliced indices to filter across 50,000+ rows instantly upon typing in the search box.
* **Custom Delegates & Rendering**: Color-coded badges for match states (`MATCHED` in emerald green, `MISSING` in soft amber/crimson, `DIFFERENCE` in indigo).
