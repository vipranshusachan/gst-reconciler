# Module Architecture

The codebase is organized into well-defined packages within `app/`:

```
app/
├── core/                   # Cross-cutting primitives (config, logging, exceptions, event bus)
│   ├── config.py           # Application settings, tolerances, directories
│   ├── logging.py          # Structured file and console logging
│   └── exceptions.py       # Domain-specific hierarchy of exceptions
│
├── domain/                 # Pure business entities & value objects (zero external deps)
│   ├── models.py           # Canonical InvoiceRecord, MatchRecord, MismatchReason
│   └── enums.py            # MatchStatus, DiscrepancyType, DocumentType
│
├── ingestion/              # Multi-format tabular data parsers
│   ├── reader_base.py      # BaseTabularReader abstraction
│   ├── excel_reader.py     # OpenPyXL & xlrd streaming reader
│   ├── csv_reader.py       # Auto-detecting CSV reader
│   └── pdf_reader.py       # Digital text layout extractor
│
├── ocr/                    # Modular OCR providers
│   ├── ocr_provider.py     # OCRProvider abstract base class
│   ├── tesseract_ocr.py    # Local Tesseract implementation
│   └── validator.py        # Post-OCR regex validation & character correction
│
├── normalization/          # Sanitization & standardization engines
│   ├── gstin.py            # GSTIN uppercase, strip, format & checksum validation
│   ├── invoice_no.py       # Invoice number trimming, punctuation cleaning
│   ├── date_parser.py      # Multi-format date normalizer
│   └── column_mapper.py    # Heuristic column detection engine & mapping profiles
│
├── reconciliation/         # Pure domain matching engine
│   ├── engine.py           # Multi-tier match pipeline (L1-L4)
│   ├── matching_rules.py   # Exact, Strong, and Normalized match rules
│   ├── fuzzy.py            # Gated Levenshtein & Token Sort matcher
│   ├── difference.py       # Decimal difference calculation & tolerance checks
│   └── classifier.py       # Discrepancy taxonomy classifier & human explanation
│
├── database/               # Local persistence & migrations
│   ├── db.py               # SQLite connection factory with WAL mode
│   ├── schema.py           # SQLAlchemy declarative tables
│   ├── repository.py       # Repository pattern for Projects, Invoices, Matches
│   └── migrations.py       # Versioned SQLite PRAGMA user_version schema manager
│
├── reporting/              # Multi-format export generation
│   ├── excel_exporter.py   # Styled OpenPyXL audit workbook generator
│   └── csv_exporter.py     # High-speed streaming CSV generator
│
├── ui/                     # PySide6 desktop GUI
│   ├── app.py              # Qt Application bootstrap & theme initialization
│   ├── main_window.py      # Shell window, sidebar, and view router
│   ├── views/              # Concrete view widgets
│   ├── models/             # QAbstractTableModel implementations
│   └── components/         # Reusable cards, status badges, diff viewers
│
└── cli/                    # Command-line interface
    └── main.py             # Headless CLI entrypoint
```
