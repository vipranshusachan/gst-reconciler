"""Canonical Domain Models for GST Reconciler."""

import uuid
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional

from app.domain.enums import DiscrepancyType, MatchLevel, MatchStatus, ReviewStatus


@dataclass
class InvoiceRecord:
    """Canonical representation of an imported invoice row."""

    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str = "source_a"  # 'source_a' (Portal 2B) or 'source_b' (Books)
    source_file: str = ""
    source_row: int = 1

    # Identifiers
    supplier_gstin: str = ""  # Normalized 15-character uppercase GSTIN
    raw_supplier_gstin: str = ""  # Exact raw imported value
    supplier_name: Optional[str] = None
    buyer_gstin: Optional[str] = None
    invoice_number: str = ""  # Cleaned alphanumeric invoice number
    raw_invoice_number: str = ""  # Exact raw imported value
    invoice_date: Optional[date] = None
    raw_invoice_date: Optional[str] = None
    invoice_type: str = "B2B"

    # Monetary Attributes (Decimal)
    taxable_value: Decimal = Decimal("0.00")
    igst: Decimal = Decimal("0.00")
    cgst: Decimal = Decimal("0.00")
    sgst: Decimal = Decimal("0.00")
    cess: Decimal = Decimal("0.00")
    total_tax: Decimal = Decimal("0.00")
    total_invoice_value: Decimal = Decimal("0.00")

    # Statutory & Status Flags
    place_of_supply: Optional[str] = None
    reverse_charge: bool = False
    is_valid_gstin: bool = True
    validation_errors: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)

    def calculate_total_tax(self) -> Decimal:
        """Compute the sum of tax components."""
        return self.igst + self.cgst + self.sgst + self.cess


@dataclass
class MatchRecord:
    """Reconciliation comparison result pairing Source A and/or Source B records."""

    match_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = ""
    match_status: MatchStatus = MatchStatus.MATCHED
    match_level: MatchLevel = MatchLevel.NONE
    confidence_score: float = 1.0

    # Linked canonical records
    record_a: Optional[InvoiceRecord] = None  # Typically Portal GSTR-2B
    record_b: Optional[InvoiceRecord] = None  # Typically Purchase Register

    # Financial differences (Record B - Record A)
    diff_taxable: Decimal = Decimal("0.00")
    diff_igst: Decimal = Decimal("0.00")
    diff_cgst: Decimal = Decimal("0.00")
    diff_sgst: Decimal = Decimal("0.00")
    diff_cess: Decimal = Decimal("0.00")
    diff_total_tax: Decimal = Decimal("0.00")
    diff_total_value: Decimal = Decimal("0.00")

    # Granular classification & explanation
    discrepancy_types: List[DiscrepancyType] = field(default_factory=list)
    explanation: str = ""

    # User review state
    review_status: ReviewStatus = ReviewStatus.OPEN
    review_note: Optional[str] = None
    reviewed_at: Optional[str] = None


@dataclass
class ReconciliationSummary:
    """Aggregated financial and count metrics for a reconciliation run."""

    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_name: str = "Default Project"
    created_at: str = ""
    source_a_file: str = ""
    source_b_file: str = ""

    # Counts
    total_records_a: int = 0
    total_records_b: int = 0
    total_processed: int = 0
    total_matched: int = 0
    total_matched_with_diff: int = 0
    total_missing_in_a: int = 0  # In Books, Missing in 2B (ITC at Risk)
    total_missing_in_b: int = 0  # In 2B, Missing in Books (Unclaimed ITC)
    total_duplicates_a: int = 0
    total_duplicates_b: int = 0
    total_invalid_data: int = 0

    # Financial Exposure Amounts
    total_taxable_a: Decimal = Decimal("0.00")
    total_taxable_b: Decimal = Decimal("0.00")
    total_tax_a: Decimal = Decimal("0.00")
    total_tax_b: Decimal = Decimal("0.00")

    # Net Discrepancies
    net_diff_taxable: Decimal = Decimal("0.00")
    net_diff_tax: Decimal = Decimal("0.00")
    itc_at_risk_amount: Decimal = Decimal("0.00")  # Tax missing in 2B
    unclaimed_itc_amount: Decimal = Decimal("0.00")  # Tax missing in Books

    # Match items
    matches: List[MatchRecord] = field(default_factory=list)

    @property
    def match_rate_percentage(self) -> float:
        if self.total_processed == 0:
            return 0.0
        return round((self.total_matched / self.total_processed) * 100, 1)


@dataclass
class MappingProfile:
    """User-saved reusable column mapping configuration."""

    profile_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    profile_name: str = ""
    description: str = ""
    mappings: Dict[str, str] = field(default_factory=dict)
    # mappings: { "source_column_name": "canonical_field_name" }
