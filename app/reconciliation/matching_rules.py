"""Multi-tier matching rules for invoice reconciliation."""

from typing import Optional

from app.domain.models import InvoiceRecord
from app.normalization.invoice_no import extract_alphanumeric_core, normalize_invoice_number
from app.reconciliation.fuzzy import is_fuzzy_match


class MatchingRule:
    """Base class for reconciliation matching passes."""

    @staticmethod
    def exact_key(rec: InvoiceRecord) -> str:
        """Level 1 Key: (GSTIN, Raw InvNo, Date)."""
        date_str = rec.invoice_date.isoformat() if rec.invoice_date else "NO_DATE"
        inv_str = rec.raw_invoice_number.strip().upper()
        return f"{rec.supplier_gstin}::{inv_str}::{date_str}"

    @staticmethod
    def strong_key(rec: InvoiceRecord) -> str:
        """Level 2 Key: (GSTIN, Alphanumeric Clean InvNo)."""
        core = extract_alphanumeric_core(rec.invoice_number or rec.raw_invoice_number)
        return f"{rec.supplier_gstin}::{core}"

    @staticmethod
    def normalized_key(rec: InvoiceRecord) -> str:
        """Level 3 Key: (GSTIN, Normalized InvNo)."""
        norm = normalize_invoice_number(rec.invoice_number or rec.raw_invoice_number)
        return f"{rec.supplier_gstin}::{norm}"

    @staticmethod
    def fuzzy_match_candidate(
        rec_a: InvoiceRecord, rec_b: InvoiceRecord, threshold: float = 0.85
    ) -> Optional[float]:
        """Check if candidate pair matches under fuzzy conditions.

        Anchors:
        - Anchor 1: Supplier GSTIN is identical AND invoice string similarity >= threshold.
        - Anchor 2: Taxable amount is identical AND invoice string similarity >= 0.80.
        """
        # Anchor 1: Same GSTIN
        if rec_a.supplier_gstin and rec_a.supplier_gstin == rec_b.supplier_gstin:
            matched, score = is_fuzzy_match(
                rec_a.raw_invoice_number, rec_b.raw_invoice_number, threshold=threshold
            )
            if matched:
                return score

        # Anchor 2: Exact same taxable value and approximate invoice string
        if rec_a.taxable_value > 0 and rec_a.taxable_value == rec_b.taxable_value:
            matched, score = is_fuzzy_match(
                rec_a.raw_invoice_number,
                rec_b.raw_invoice_number,
                threshold=max(0.80, threshold - 0.05),
            )
            if matched:
                return score

        return None
