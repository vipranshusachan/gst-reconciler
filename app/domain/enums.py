"""Domain Enums for GST Reconciler."""

from enum import Enum

class MatchStatus(str, Enum):
    """High-level classification of a reconciliation result."""
    MATCHED = "MATCHED"
    MATCHED_WITH_DIFFERENCE = "MATCHED_WITH_DIFFERENCE"
    MISSING_IN_SOURCE_A = "MISSING_IN_SOURCE_A"  # In Books, missing in Portal 2B (ITC at Risk)
    MISSING_IN_SOURCE_B = "MISSING_IN_SOURCE_B"  # In Portal 2B, missing in Books (Unclaimed ITC)
    DUPLICATE = "DUPLICATE"
    INVALID_DATA = "INVALID_DATA"


class MatchLevel(str, Enum):
    """Specific matching rule / strategy that matched the records."""
    EXACT = "EXACT"                  # GSTIN + Exact InvNo + Date + Amounts
    STRONG = "STRONG"                # GSTIN + Cleaned InvNo + Amounts
    NORMALIZED = "NORMALIZED"        # GSTIN + Cleaned InvNo + Date window
    FUZZY = "FUZZY"                  # Token similarity >= threshold
    NONE = "NONE"


class DiscrepancyType(str, Enum):
    """Granular diagnostic issue categories."""
    TAXABLE_VALUE_MISMATCH = "TAXABLE_VALUE_MISMATCH"
    IGST_MISMATCH = "IGST_MISMATCH"
    CGST_MISMATCH = "CGST_MISMATCH"
    SGST_MISMATCH = "SGST_MISMATCH"
    CESS_MISMATCH = "CESS_MISMATCH"
    TOTAL_VALUE_MISMATCH = "TOTAL_VALUE_MISMATCH"
    DATE_MISMATCH = "DATE_MISMATCH"
    GSTIN_MISMATCH = "GSTIN_MISMATCH"
    INVOICE_NUMBER_MISMATCH = "INVOICE_NUMBER_MISMATCH"
    DUPLICATE_IN_SOURCE = "DUPLICATE_IN_SOURCE"
    MISSING_IN_PORTAL_2B = "MISSING_IN_PORTAL_2B"
    MISSING_IN_PURCHASE_REGISTER = "MISSING_IN_PURCHASE_REGISTER"
    INVALID_GSTIN = "INVALID_GSTIN"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"


class ReviewStatus(str, Enum):
    """Accountant review and resolution states."""
    OPEN = "OPEN"
    REVIEWED = "REVIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    IGNORED = "IGNORED"


class DocumentType(str, Enum):
    """GST tax document types."""
    B2B = "B2B"          # Standard B2B Invoice
    CDNR = "CDNR"        # Credit / Debit Note Registered
    CDNUR = "CDNUR"      # Credit / Debit Note Unregistered
    B2BUR = "B2BUR"      # B2B Reverse Charge Unregistered
    SEZWP = "SEZWP"      # SEZ Supplies with Payment
    SEZWOP = "SEZWOP"    # SEZ Supplies without Payment
    IMPG = "IMPG"        # Import of Goods
    IMPS = "IMPS"        # Import of Services
