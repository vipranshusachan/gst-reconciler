"""Unit tests for Decimal difference and tolerance calculations."""

from decimal import Decimal
from app.core.config import Tolerances
from app.domain.models import InvoiceRecord
from app.reconciliation.difference import calculate_differences, round_currency

def test_round_currency():
    assert round_currency(Decimal("100.456")) == Decimal("100.46")
    assert round_currency(Decimal("100.454")) == Decimal("100.45")


def test_calculate_differences_exact_match():
    rec_a = InvoiceRecord(
        taxable_value=Decimal("10000.00"),
        cgst=Decimal("900.00"),
        sgst=Decimal("900.00"),
        igst=Decimal("0.00"),
        total_invoice_value=Decimal("11800.00"),
    )
    rec_b = InvoiceRecord(
        taxable_value=Decimal("10000.00"),
        cgst=Decimal("900.00"),
        sgst=Decimal("900.00"),
        igst=Decimal("0.00"),
        total_invoice_value=Decimal("11800.00"),
    )

    tols = Tolerances(taxable=Decimal("5.00"), total_tax=Decimal("2.00"))
    diff_taxable, diff_igst, diff_cgst, diff_sgst, diff_cess, diff_tax, diff_val, is_within = calculate_differences(
        rec_a, rec_b, tols
    )

    assert diff_taxable == Decimal("0.00")
    assert diff_tax == Decimal("0.00")
    assert is_within is True


def test_calculate_differences_within_tolerance():
    rec_a = InvoiceRecord(
        taxable_value=Decimal("10000.00"),
        cgst=Decimal("900.00"),
        sgst=Decimal("900.00"),
        total_invoice_value=Decimal("11800.00"),
    )
    rec_b = InvoiceRecord(
        taxable_value=Decimal("10001.50"),  # +1.50 diff (within 5.0)
        cgst=Decimal("900.50"),             # +0.50 diff (within 2.0)
        sgst=Decimal("900.50"),             # +0.50 diff (within 2.0)
        total_invoice_value=Decimal("11802.50"),
    )

    tols = Tolerances(taxable=Decimal("5.00"), cgst=Decimal("2.00"), sgst=Decimal("2.00"), total_tax=Decimal("2.00"))
    *_, is_within = calculate_differences(rec_a, rec_b, tols)
    assert is_within is True


def test_calculate_differences_exceeding_tolerance():
    rec_a = InvoiceRecord(
        taxable_value=Decimal("10000.00"),
        cgst=Decimal("900.00"),
        sgst=Decimal("900.00"),
    )
    rec_b = InvoiceRecord(
        taxable_value=Decimal("10500.00"),  # +500 diff (exceeds 5.0)
        cgst=Decimal("945.00"),
        sgst=Decimal("945.00"),
    )

    tols = Tolerances(taxable=Decimal("5.00"), cgst=Decimal("2.00"))
    *_, is_within = calculate_differences(rec_a, rec_b, tols)
    assert is_within is False
