"""Financial and tax difference calculation engine using Decimal arithmetic."""

from decimal import Decimal, ROUND_HALF_UP
from typing import Tuple
from app.core.config import Tolerances
from app.domain.models import InvoiceRecord

def round_currency(val: Decimal) -> Decimal:
    """Round decimal value to 2 decimal places using standard half-up rounding."""
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_differences(
    rec_a: InvoiceRecord,
    rec_b: InvoiceRecord,
    tolerances: Tolerances
) -> Tuple[Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool]:
    """Calculate monetary differences: Record B (Books) minus Record A (Portal).
    
    Returns:
        (diff_taxable, diff_igst, diff_cgst, diff_sgst, diff_cess, diff_total_tax, diff_total_val, is_within_tolerance)
    """
    diff_taxable = round_currency(rec_b.taxable_value - rec_a.taxable_value)
    diff_igst = round_currency(rec_b.igst - rec_a.igst)
    diff_cgst = round_currency(rec_b.cgst - rec_a.cgst)
    diff_sgst = round_currency(rec_b.sgst - rec_a.sgst)
    diff_cess = round_currency(rec_b.cess - rec_a.cess)

    tax_a = rec_a.calculate_total_tax()
    tax_b = rec_b.calculate_total_tax()
    diff_total_tax = round_currency(tax_b - tax_a)

    val_a = rec_a.total_invoice_value if rec_a.total_invoice_value else (rec_a.taxable_value + tax_a)
    val_b = rec_b.total_invoice_value if rec_b.total_invoice_value else (rec_b.taxable_value + tax_b)
    diff_total_val = round_currency(val_b - val_a)

    # Check whether all differences are within user-configured tolerances
    within_taxable = abs(diff_taxable) <= tolerances.taxable
    within_igst = abs(diff_igst) <= tolerances.igst
    within_cgst = abs(diff_cgst) <= tolerances.cgst
    within_sgst = abs(diff_sgst) <= tolerances.sgst
    within_cess = abs(diff_cess) <= tolerances.cess
    within_tax = abs(diff_total_tax) <= tolerances.total_tax
    within_val = abs(diff_total_val) <= tolerances.total_value

    is_within = (
        within_taxable and
        within_igst and
        within_cgst and
        within_sgst and
        within_cess and
        within_tax and
        within_val
    )

    return (
        diff_taxable,
        diff_igst,
        diff_cgst,
        diff_sgst,
        diff_cess,
        diff_total_tax,
        diff_total_val,
        is_within
    )
