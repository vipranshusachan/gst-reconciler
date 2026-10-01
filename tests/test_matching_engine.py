"""Comprehensive unit tests for ReconciliationEngine multi-tier matching."""

from datetime import date
from decimal import Decimal

from app.domain.enums import MatchLevel, MatchStatus
from app.domain.models import InvoiceRecord
from app.reconciliation.engine import ReconciliationEngine


def test_engine_exact_match():
    rec_a = InvoiceRecord(
        record_id="rec-a-1",
        supplier_gstin="27AABCT3518Q1Z6",
        raw_invoice_number="INV/2026/001",
        invoice_number="INV/2026/1",
        invoice_date=date(2026, 9, 1),
        taxable_value=Decimal("10000.00"),
        cgst=Decimal("900.00"),
        sgst=Decimal("900.00"),
    )
    rec_b = InvoiceRecord(
        record_id="rec-b-1",
        supplier_gstin="27AABCT3518Q1Z6",
        raw_invoice_number="INV/2026/001",
        invoice_number="INV/2026/1",
        invoice_date=date(2026, 9, 1),
        taxable_value=Decimal("10000.00"),
        cgst=Decimal("900.00"),
        sgst=Decimal("900.00"),
    )

    engine = ReconciliationEngine()
    summary = engine.reconcile([rec_a], [rec_b])

    assert summary.total_matched == 1
    assert summary.matches[0].match_status == MatchStatus.MATCHED
    assert summary.matches[0].match_level == MatchLevel.EXACT


def test_engine_strong_normalized_match():
    # Source A has "INV/0042", Source B has "INV-42"
    rec_a = InvoiceRecord(
        record_id="rec-a-2",
        supplier_gstin="27AABCT3518Q1Z6",
        raw_invoice_number="INV/0042",
        invoice_number="INV/42",
        taxable_value=Decimal("15000.00"),
        igst=Decimal("2700.00"),
    )
    rec_b = InvoiceRecord(
        record_id="rec-b-2",
        supplier_gstin="27AABCT3518Q1Z6",
        raw_invoice_number="INV-42",
        invoice_number="INV/42",
        taxable_value=Decimal("15000.00"),
        igst=Decimal("2700.00"),
    )

    engine = ReconciliationEngine()
    summary = engine.reconcile([rec_a], [rec_b])

    assert summary.total_matched == 1
    assert summary.matches[0].match_status == MatchStatus.MATCHED
    assert summary.matches[0].match_level in (MatchLevel.EXACT, MatchLevel.STRONG)


def test_engine_missing_in_source_a_and_b():
    # Rec A is in 2B only
    rec_a = InvoiceRecord(
        record_id="rec-a-only",
        supplier_gstin="27AABCT3518Q1Z6",
        raw_invoice_number="PORTAL-INV-99",
        invoice_number="PORTAL/INV/99",
        taxable_value=Decimal("8000.00"),
        igst=Decimal("1440.00"),
    )
    # Rec B is in Books only
    rec_b = InvoiceRecord(
        record_id="rec-b-only",
        supplier_gstin="29AAACB2002M1ZR",
        raw_invoice_number="BOOKS-INV-88",
        invoice_number="BOOKS/INV/88",
        taxable_value=Decimal("5000.00"),
        cgst=Decimal("450.00"),
        sgst=Decimal("450.00"),
    )

    engine = ReconciliationEngine()
    summary = engine.reconcile([rec_a], [rec_b])

    assert summary.total_missing_in_a == 1  # In Books, missing in 2B (ITC at Risk)
    assert summary.total_missing_in_b == 1  # In 2B, missing in Books
    assert summary.itc_at_risk_amount == Decimal("900.00")
    assert summary.unclaimed_itc_amount == Decimal("1440.00")
