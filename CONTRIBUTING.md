# Contributing to GST Reconciler

Thank you for your interest in contributing to **GST Reconciler**! We welcome community contributions to enhance features, improve performance, expand accounting ERP mappings, and squash bugs.

---

## 📜 Code of Conduct

All contributors and participants are expected to adhere to our [Code of Conduct](file:///CODE_OF_CONDUCT.md).

---

## 🛠️ Development Setup

1. **Prerequisites**:
   * Python 3.11, 3.12, or 3.13
   * Git
   * Windows 10/11 (or Wine/Linux for headless engine testing)

2. **Clone & Environment Setup**:
   ```bash
   git clone https://github.com/vipranshusachan/gst-reconciler.git
   cd gst-reconciler
   python -m venv venv
   venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Running Quality Checks**:
   ```bash
   pytest tests/
   ruff check .
   ruff format --check .
   mypy app/
   ```

---

## 🔄 Git Workflow & Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/):
* `feat:` A new feature or capability
* `fix:` A bug fix
* `docs:` Documentation improvements
* `test:` Adding or updating automated tests
* `refactor:` Code restructuring without functional change
* `perf:` Performance optimizations
* `build:` Packaging, CI, or dependency updates

---

## 🧪 Testing Guidelines

* Every business logic change (especially within `app/reconciliation/` or `app/normalization/`) must be covered by comprehensive unit tests.
* **NEVER commit real taxpayer data, client PANs, or live GSTINs.** Always use synthetic mock data adhering to the generator in `tests/fixtures/`.

---

## 📬 Pull Request Process

1. Fork the repository and create your feature branch: `git checkout -b feat/tally-prime-mapper`.
2. Ensure all tests pass (`pytest`) and linters pass (`ruff`).
3. Update relevant documentation in `docs/` if architecture or features changed.
4. Open a Pull Request following the PR template.
