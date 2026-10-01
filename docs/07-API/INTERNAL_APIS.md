# Internal Programmatic APIs

## 1. Python Domain Service Interface

The core business logic can be embedded directly into Python scripts, automated worker routines, or future REST endpoints:

```python
from pathlib import Path
from app.application.service import ReconciliationService
from app.domain.models import Tolerances

# Initialize service
service = ReconciliationService()

# Ingest and map files
source_a_invoices = service.ingest_file(
    file_path=Path("tests/fixtures/gstr2b_sample.xlsx"),
    source_id="source_a",
    sheet_name="B2B",
    custom_mapping={"GSTIN of Supplier": "supplier_gstin", "Invoice number": "invoice_number"},
)

source_b_invoices = service.ingest_file(
    file_path=Path("tests/fixtures/purchase_register_sample.xlsx"), source_id="source_b"
)

# Execute reconciliation
tolerances = Tolerances(taxable=5.0, tax=2.0)
summary = service.reconcile(
    records_a=source_a_invoices, records_b=source_b_invoices, tolerances=tolerances
)

# Access summary metrics
print(f"Total matched: {summary.total_matched}")
print(f"ITC at risk: {summary.total_missing_in_a_tax}")

# Export report
service.export_excel(summary, Path("output/reconciliation_report.xlsx"))
```

---

## 2. CLI Command Interface

```bash
# Run headless reconciliation
gst-reconciler reconcile \
    --source-a data/gstr2b.xlsx \
    --source-b data/tally_purchase.xlsx \
    --taxable-tolerance 5.0 \
    --tax-tolerance 2.0 \
    --export output/audit_report.xlsx
```
