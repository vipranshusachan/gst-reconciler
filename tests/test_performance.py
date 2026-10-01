"""Performance and stress benchmark for large reconciliation datasets."""

import time
from datetime import date, timedelta
from decimal import Decimal

from app.core.config import Tolerances
from app.domain.models import InvoiceRecord
from app.reconciliation.engine import ReconciliationEngine


def test_large_dataset_performance():
    """Benchmark reconciliation speed on 10,000 invoices."""
    records_a = []
    records_b = []

    base_date = date(2026, 9, 1)

    # 10,000 synthetic records
    for i in range(10000):
        gstin = f"27AABC{i % 500:04d}Q1Z6"
        inv_no_a = f"INV/2026/{i}"
        inv_no_b = f"INV-2026-{i}"  # Format variation
        taxable = Decimal(f"{5000 + (i % 1000)}.00")
        cgst = (taxable * Decimal("0.09")).quantize(Decimal("0.01"))
        sgst = (taxable * Decimal("0.09")).quantize(Decimal("0.01"))

        rec_a = InvoiceRecord(
            record_id=f"a-{i}",
            source_id="source_a",
            supplier_gstin=gstin,
            raw_invoice_number=inv_no_a,
            invoice_number=f"INV/2026/{i}",
            invoice_date=base_date + timedelta(days=i % 30),
            taxable_value=taxable,
            cgst=cgst,
            sgst=sgst,
        )
        rec_b = InvoiceRecord(
            record_id=f"b-{i}",
            source_id="source_b",
            supplier_gstin=gstin,
            raw_invoice_number=inv_no_b,
            invoice_number=f"INV/2026/{i}",
            invoice_date=base_date + timedelta(days=i % 30),
            taxable_value=taxable,
            cgst=cgst,
            sgst=sgst,
        )
        records_a.append(rec_a)
        records_b.append(rec_b)

    engine = ReconciliationEngine(
        tolerances=Tolerances(taxable=Decimal("5.00"), total_tax=Decimal("2.00"))
    )

    start_time = time.perf_counter()
    summary = engine.reconcile(records_a, records_b)
    elapsed = time.perf_counter() - start_time

    print(
        f"\n[BENCHMARK] Reconciled 20,000 total records in {elapsed:.3f} seconds ({len(records_a) / elapsed:.0f} rec/sec)"
    )
    assert summary.total_matched == 10000
    # Must complete in under 2.5 seconds
    assert elapsed < 2.5
