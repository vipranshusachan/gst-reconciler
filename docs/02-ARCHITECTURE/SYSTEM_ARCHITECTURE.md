# System Architecture

## 1. Architectural Philosophy & Boundaries

GST Reconciler follows a **Clean, Modular, Offline-First Architecture** designed around strict domain boundaries. The system strictly isolates the presentation layer (PySide6 Desktop UI & CLI) from the core business domain (Reconciliation Engine, Ingestion, Normalization, Persistence).

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│   ┌───────────────────────────┐  ┌─────────────────┐   │
│   │     PySide6 GUI App       │  │  Headless CLI   │   │
│   │  (Views, Models, Widgets) │  │   (Click/Arg)   │   │
│   └─────────────┬─────────────┘  └────────┬────────┘   │
└─────────────────┼─────────────────────────┼────────────┘
                  ▼                         ▼
┌────────────────────────────────────────────────────────┐
│                   Application Layer                    │
│   ┌────────────────────────────────────────────────┐   │
│   │             Reconciliation Service             │   │
│   │    - Orchestration, Worker Threads, Events     │   │
│   │    - Project & Settings Management             │   │
│   └───────────────────────┬────────────────────────┘   │
└───────────────────────────┼────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                      Domain Layer                      │
│   ┌───────────────────┐  ┌─────────────────────────┐   │
│   │ Ingestion Pipeline│  │ Normalization Engine    │   │
│   │  - Excel/CSV/PDF  │  │  - GSTIN, InvNo, Date   │   │
│   └─────────┬─────────┘  └────────────┬────────────┘   │
│             │                         │                │
│             ▼                         ▼                │
│   ┌────────────────────────────────────────────────┐   │
│   │           Core Reconciliation Engine           │   │
│   │  - Multi-tier matching (Exact, Strong, Fuzzy)  │   │
│   │  - Tolerance & difference calculation          │   │
│   │  - Granular mismatch classification            │   │
│   └───────────────────────┬────────────────────────┘   │
└───────────────────────────┼────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                   │
│   ┌────────────────────┐  ┌────────────────────────┐   │
│   │   SQLite Database  │  │    Export Engine       │   │
│   │   - WAL, Migrations│  │    - OpenPyXL, CSV     │   │
│   └────────────────────┘  └────────────────────────┘   │
│   ┌────────────────────┐  ┌────────────────────────┐   │
│   │ OCR Abstraction    │  │ Structured Logging     │   │
│   │ - Tesseract/Plumber│  │ - File & Console logs  │   │
│   └────────────────────┘  └────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```

---

## 2. Core Architectural Pillars

1. **Zero External Network Dependencies**: All computations, parsers, and data storage execute locally.
2. **Headless Engine Independence**: The entire reconciliation engine can be imported as a pure Python library without Qt installed.
3. **Immutability of Source Data**: Imported source rows are preserved in their raw format alongside normalized and derived match attributes.
4. **Exact Precision**: Financial values are converted and held in `Decimal` objects to prevent floating-point calculation errors.
5. **Thread Safety**: Long-running ingestion, reconciliation, and export jobs execute on background worker threads (`QThread` in GUI, asynchronous executors in CLI) to ensure the UI remains 100% responsive.
