# Testing Strategy

## 1. Test Pyramid & Methodologies

The application enforces a 4-tier testing hierarchy:

```text
       ▲
      / \        End-to-End Tests (Full Ingestion -> Matching -> Export)
     /   \
    /─────\      Integration Tests (Excel/CSV Readers, SQLite Migrations, OCR Provider)
   /       \
  /─────────\    Unit Tests (GSTIN validator, Date parser, Tolerances, Matching Rules)
```

---

## 2. Testing Principles

1. **Deterministic Accuracy**: Matching calculations and currency differences must be 100% reproducible across test runs.
2. **Zero Real Taxpayer Data in Repo**: All tests operate strictly against synthetic, programmatically generated mock datasets.
3. **High Code Coverage**: Target minimum 90% branch coverage on domain models, normalization, and reconciliation engine modules.
4. **Automated CI Enforcement**: All PRs must pass `pytest -v` across Python 3.11, 3.12, and 3.13 on Windows runners.
