# ADR 0001: Desktop UI Framework Selection (PySide6 / Qt)

## Status
Accepted

## Context
GST Reconciler is a desktop application intended for Indian accounting practitioners, business owners, and tax professionals. The application must:
1. Render high-density tables containing thousands of invoice records with smooth scrolling and dynamic filtering.
2. Provide interactive dashboards, data visualizer charts, progress bars, and multi-step modal wizards.
3. Native Windows look-and-feel with standard file dialogs, keyboard shortcuts, and responsive layouts.
4. Run 100% offline without requiring Node.js, Electron runtime bloat, or an embedded browser overhead.
5. Compile reliably into a standalone Windows `.exe` using PyInstaller or Nuitka.

Evaluated options:
* **PySide6 (Qt for Python)**: Official Qt company bindings for Qt 6. High performance, native C++ rendering engine, virtualized table views (`QTableView`, `QAbstractTableModel`), thread-safe signal/slot mechanism (`QThread`, `Signal`, `Slot`), rich widget library, low memory footprint (~50-80MB RAM vs 350MB+ for Electron).
* **Tkinter / CustomTkinter**: Lightweight, built into Python, but limited virtualized table performance for 100k+ rows, lack of modern enterprise layout containers, limited charting.
* **Electron + Python backend**: High memory overhead (Chromium + Node + Python runtime), large binary size (>200MB), complex multi-process lifecycle management on Windows.
* **Flet / Flutter Python**: Immature desktop support for complex nested data grids and Windows enterprise accessibility.

## Decision
We choose **PySide6 (Qt 6 for Python)** as the primary UI technology for GST Reconciler.

## Consequences
* **Positive**:
  - Virtualized table models (`QAbstractTableModel`) allow instant rendering of 100,000+ records with microsecond response times.
  - Native Windows desktop integration (native file dialogs, taskbar progress, DPI scaling).
  - Clean separation of UI from business logic via Qt Signals and Slots.
  - Rock-solid PyInstaller packaging with official Qt support.
* **Negative**:
  - Requires licensing awareness (PySide6 is licensed under LGPLv3; our application architecture keeps UI modules cleanly decoupled, permitting Apache-2.0 or MIT for application business logic).
