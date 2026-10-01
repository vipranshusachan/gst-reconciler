# Canonical Data Model

## 1. InvoiceRecord Entity

The `InvoiceRecord` entity serves as the canonical representation of any tax document across GSTR-2B, GSTR-1, Purchase Registers, and Sales Ledgers.

```python
from dataclasses import dataclass, field
from decimal import Decimal
from datetime import date
from typing import Optional, Dict, Any


@dataclass
class InvoiceRecord:
    # System Identifiers
    record_id: str  # UUID v4
    source_id: str  # 'source_a' or 'source_b'
    source_file: str  # Original filename
    source_row: int  # 1-indexed source row number

    # Core Identifiers
    supplier_gstin: str  # 15-character normalized GSTIN
    supplier_name: Optional[str]  # Trade / Legal Name
    buyer_gstin: Optional[str]  # Recipient GSTIN
    invoice_number: str  # Normalized alphanumeric invoice string
    raw_invoice_number: str  # Untouched raw string as imported
    invoice_date: Optional[date]  # Standardized ISO date
    invoice_type: str  # 'B2B', 'CDNR', 'SEZWP', 'SEZWOP', etc.

    # Financial Attributes (Strict Decimal)
    taxable_value: Decimal = Decimal("0.00")
    igst: Decimal = Decimal("0.00")
    cgst: Decimal = Decimal("0.00")
    sgst: Decimal = Decimal("0.00")
    cess: Decimal = Decimal("0.00")
    total_tax: Decimal = Decimal("0.00")
    total_invoice_value: Decimal = Decimal("0.00")

    # Statutory & Geographical Attributes
    place_of_supply: Optional[str] = None  # 2-digit state code or name
    reverse_charge: bool = False
    itc_eligibility: Optional[str] = None  # 'GSTR-2B ITC Available', etc.

    # Validation & Raw Snapshot
    is_valid_gstin: bool = True
    validation_errors: list[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)
```

---

## 2. MatchRecord Entity

The `MatchRecord` represents the reconciliation result of joining or isolating records from Source A and Source B.

```python
@dataclass
class MatchRecord:
    match_id: str
    project_id: str
    match_status: str  # MATCHED, MATCHED_WITH_DIFFERENCE, MISSING_IN_SOURCE_A, etc.
    match_level: str  # EXACT, STRONG, NORMALIZED, FUZZY, NONE
    confidence_score: float  # 0.0 to 1.0

    # Linked Entities
    record_a: Optional[InvoiceRecord]  # Record from Source A (e.g. Portal GSTR-2B)
    record_b: Optional[InvoiceRecord]  # Record from Source B (e.g. ERP Purchase Register)

    # Financial Deltas (Record B minus Record A)
    diff_taxable: Decimal = Decimal("0.00")
    diff_igst: Decimal = Decimal("0.00")
    diff_cgst: Decimal = Decimal("0.00")
    diff_sgst: Decimal = Decimal("0.00")
    diff_cess: Decimal = Decimal("0.00")
    diff_total_tax: Decimal = Decimal("0.00")
    diff_total_value: Decimal = Decimal("0.00")

    # Diagnostics & Explanation
    discrepancy_types: list[str] = field(default_factory=list)
    explanation: str = ""

    # User Review State
    review_status: str = "OPEN"  # OPEN, REVIEWED, ACCEPTED, REJECTED, IGNORED
    review_note: Optional[str] = None
    reviewed_at: Optional[str] = None
```
