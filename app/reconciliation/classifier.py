"""Discrepancy classification and explanation engine."""

from decimal import Decimal
from typing import List, Tuple

from app.core.config import Tolerances
from app.domain.enums import DiscrepancyType
from app.domain.models import InvoiceRecord


class DiscrepancyClassifier:
    """Classifies differences into granular discrepancy types and formats plain English explanations."""

    @classmethod
    def classify(
        cls,
        rec_a: InvoiceRecord,
        rec_b: InvoiceRecord,
        diff_taxable: Decimal,
        diff_igst: Decimal,
        diff_cgst: Decimal,
        diff_sgst: Decimal,
        diff_cess: Decimal,
        diff_total_tax: Decimal,
        diff_total_val: Decimal,
        tolerances: Tolerances,
        match_level: str,
    ) -> Tuple[List[DiscrepancyType], str]:
        """Examine differences and produce discrepancy tags with a human explanation."""
        discrepancies: List[DiscrepancyType] = []
        notes: List[str] = []

        if abs(diff_taxable) > tolerances.taxable:
            discrepancies.append(DiscrepancyType.TAXABLE_VALUE_MISMATCH)
            notes.append(
                f"Taxable value differs by ₹{diff_taxable:+.2f} (exceeds ₹{tolerances.taxable} tolerance)"
            )

        if abs(diff_igst) > tolerances.igst:
            discrepancies.append(DiscrepancyType.IGST_MISMATCH)
            notes.append(f"IGST differs by ₹{diff_igst:+.2f}")

        if abs(diff_cgst) > tolerances.cgst:
            discrepancies.append(DiscrepancyType.CGST_MISMATCH)
            notes.append(f"CGST differs by ₹{diff_cgst:+.2f}")

        if abs(diff_sgst) > tolerances.sgst:
            discrepancies.append(DiscrepancyType.SGST_MISMATCH)
            notes.append(f"SGST differs by ₹{diff_sgst:+.2f}")

        if abs(diff_cess) > tolerances.cess:
            discrepancies.append(DiscrepancyType.CESS_MISMATCH)
            notes.append(f"Cess differs by ₹{diff_cess:+.2f}")

        # Date comparison
        if rec_a.invoice_date and rec_b.invoice_date:
            days_diff = abs((rec_b.invoice_date - rec_a.invoice_date).days)
            if days_diff > tolerances.date_days:
                discrepancies.append(DiscrepancyType.DATE_MISMATCH)
                notes.append(
                    f"Invoice date differs by {days_diff} days ({rec_a.invoice_date} vs {rec_b.invoice_date})"
                )

        # Invoice number formatting difference
        if rec_a.raw_invoice_number.strip().upper() != rec_b.raw_invoice_number.strip().upper():
            if match_level in ("STRONG", "NORMALIZED", "FUZZY"):
                discrepancies.append(DiscrepancyType.INVOICE_NUMBER_MISMATCH)
                notes.append(
                    f"Invoice formatting variation: '{rec_a.raw_invoice_number}' in 2B vs '{rec_b.raw_invoice_number}' in Books"
                )

        # GSTIN comparison
        if rec_a.supplier_gstin != rec_b.supplier_gstin:
            discrepancies.append(DiscrepancyType.GSTIN_MISMATCH)
            notes.append(
                f"Supplier GSTIN differs: '{rec_a.supplier_gstin}' vs '{rec_b.supplier_gstin}'"
            )

        if not discrepancies:
            if abs(diff_taxable) > Decimal("0.00") or abs(diff_total_tax) > Decimal("0.00"):
                explanation = (
                    f"Matched with minor round-off differences within tolerance "
                    f"(Taxable delta: ₹{diff_taxable:+.2f}, Tax delta: ₹{diff_total_tax:+.2f})"
                )
            else:
                explanation = "Matched: Perfect match across all fields."
        else:
            explanation = "Differences detected: " + "; ".join(notes)

        return discrepancies, explanation
