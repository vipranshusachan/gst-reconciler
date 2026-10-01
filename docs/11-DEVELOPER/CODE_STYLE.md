# Code Style & Quality Standards

## 1. Tooling & Linters

We use **Ruff** for high-speed Python linting and formatting, alongside **Mypy** for type checking.

### Configuration (`pyproject.toml`):
* Line length: 100 characters.
* Target Python version: Python 3.11+.
* Type checking: Strict typing required for domain and reconciliation modules.

## 2. Naming Conventions

* Classes: PascalCase (`InvoiceRecord`, `ReconciliationEngine`)
* Functions & Variables: snake_case (`normalize_gstin`, `taxable_value`)
* Constants: UPPER_SNAKE_CASE (`DEFAULT_TAXABLE_TOLERANCE`)
* Qt UI Classes: Suffix with `View`, `Dialog`, or `Widget` (`DashboardView`, `ComparisonModalDialog`)
