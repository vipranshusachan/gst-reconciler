# Developer Setup Guide

## 1. Prerequisites

* Windows 10/11 64-bit (or Linux/macOS for core engine development)
* Python 3.11, 3.12, or 3.13
* Git

---

## 2. Installation Steps

```bash
# Clone the repository
git clone https://github.com/opensource/gst-reconciler.git
cd gst-reconciler

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install package in editable mode with development dependencies
pip install -e ".[dev]"
```

---

## 3. Running Verification Suite

```bash
# Run all unit and integration tests
pytest -v

# Run linter
ruff check .

# Run format check
ruff format --check .

# Run static type checking
mypy app/
```

---

## 4. Running the Desktop UI Locally

```bash
python -m app.ui.app
# or using the CLI entry point:
gst-reconciler gui
```
