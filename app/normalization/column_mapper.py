"""Intelligent Column Mapping Engine with heuristic detection and profiles."""

import re
from typing import Dict, List, Optional, Tuple

from app.domain.models import MappingProfile

# Canonical target field definitions
CANONICAL_FIELDS = {
    "supplier_gstin": "Supplier GSTIN / UIN",
    "supplier_name": "Supplier / Trade Name",
    "invoice_number": "Invoice / Bill Number",
    "invoice_date": "Invoice Date",
    "taxable_value": "Taxable Value (Assessable Amount)",
    "igst": "Integrated Tax (IGST)",
    "cgst": "Central Tax (CGST)",
    "sgst": "State / UT Tax (SGST)",
    "cess": "Compensation Cess",
    "total_invoice_value": "Total Invoice Value (Gross)",
    "place_of_supply": "Place of Supply (POS)",
    "invoice_type": "Invoice Type (B2B, CDNR, etc.)",
}

# Heuristic synonym and regex patterns
FIELD_PATTERNS = {
    "supplier_gstin": [
        r"^gstin(?:[_\s]*uin)?(?:[_\s]*of[_\s]*supplier)?$",
        r"^supplier[_\s]*gstin$",
        r"^vendor[_\s]*gstin$",
        r"^party[_\s]*gstin$",
        r"^gst[_\s]*no\.?$",
        r"^gstin$",
        r"^gst$",
    ],
    "supplier_name": [
        r"^supplier[_\s]*name$",
        r"^trade[_\s]*name$",
        r"^legal[_\s]*name$",
        r"^party[_\s]*name$",
        r"^vendor[_\s]*name$",
        r"^name[_\s]*of[_\s]*supplier$",
        r"^party$",
        r"^vendor$",
    ],
    "invoice_number": [
        r"^invoice[_\s]*no(?:umber|\.)?$",
        r"^inv[_\s]*no\.?$",
        r"^bill[_\s]*no\.?$",
        r"^doc(?:ument)?[_\s]*no\.?$",
        r"^voucher[_\s]*no\.?$",
        r"^invoice[_\s]*num$",
        r"^invoice$",
    ],
    "invoice_date": [
        r"^invoice[_\s]*date$",
        r"^inv[_\s]*date$",
        r"^bill[_\s]*date$",
        r"^doc(?:ument)?[_\s]*date$",
        r"^voucher[_\s]*date$",
        r"^date$",
    ],
    "taxable_value": [
        r"^taxable[_\s]*(?:value|amount|amt)$",
        r"^taxable$",
        r"^assessable[_\s]*value$",
        r"^base[_\s]*amount$",
        r"^taxable[_\s]*amt\.?$",
    ],
    "igst": [
        r"^igst[_\s]*(?:amount|amt)?$",
        r"^integrated[_\s]*tax(?:[_\s]*amount)?$",
        r"^integrated[_\s]*gst$",
        r"^igst$",
    ],
    "cgst": [
        r"^cgst[_\s]*(?:amount|amt)?$",
        r"^central[_\s]*tax(?:[_\s]*amount)?$",
        r"^central[_\s]*gst$",
        r"^cgst$",
    ],
    "sgst": [
        r"^state(?:_ut)?_tax(?:_amount|_amt)?$",
        r"^state(?:_ut)?_gst$",
        r"^sgst(?:_utgst)?(?:_amount|_amt)?$",
        r"^sgst$",
        r"^utgst$",
        r"^state_tax$",
    ],
    "cess": [
        r"^cess(?:_amount|_amt)?$",
        r"^compensation_cess$",
        r"^cess$",
    ],
    "total_invoice_value": [
        r"^total(?:_invoice)?(?:_value|_amount)?$",
        r"^invoice_value$",
        r"^inv_value$",
        r"^gross(?:_total|_amount)$",
        r"^bill_amount$",
        r"^total$",
    ],
    "place_of_supply": [
        r"^place_of_supply$",
        r"^pos$",
        r"^state_code$",
        r"^supply_place$",
    ],
    "invoice_type": [
        r"^invoice_type$",
        r"^inv_type$",
        r"^document_type$",
        r"^doc_type$",
    ],
}


class ColumnMapper:
    """Detects and maps source spreadsheet headers to canonical invoice fields."""

    @staticmethod
    def clean_header(header: str) -> str:
        """Sanitize header string for pattern matching."""
        if not header:
            return ""
        # Lowercase, trim, strip punctuation and extra spaces
        h = header.strip().lower()
        h = re.sub(r"[\r\n\t]+", " ", h)
        h = re.sub(r"[()\[\]./\\-]", "_", h)
        h = re.sub(r"[_\s]+", "_", h).strip("_")
        return h

    @classmethod
    def detect_mappings(cls, headers: List[str]) -> Tuple[Dict[str, str], Dict[str, float]]:
        """Map raw header names to canonical field keys.

        Returns:
            (mappings, confidences)
            where mappings = { "source_header": "canonical_field" }
                  confidences = { "canonical_field": 0.95 }
        """
        mappings: Dict[str, str] = {}
        confidences: Dict[str, float] = {}
        used_canonical: set = set()

        # Pass 1: Exact and regex matching
        for raw_header in headers:
            cleaned = cls.clean_header(raw_header)
            if not cleaned:
                continue

            best_match: Optional[str] = None
            best_score: float = 0.0

            for canonical_key, patterns in FIELD_PATTERNS.items():
                if canonical_key in used_canonical:
                    continue

                for pattern in patterns:
                    if re.match(pattern, cleaned):
                        score = 1.0 if pattern.startswith(f"^{cleaned}$") else 0.95
                        if score > best_score:
                            best_match = canonical_key
                            best_score = score
                        break

            if best_match and best_score >= 0.80:
                mappings[raw_header] = best_match
                confidences[best_match] = best_score
                used_canonical.add(best_match)

        # Pass 2: Substring matching for unmapped essential fields
        for raw_header in headers:
            if raw_header in mappings:
                continue
            cleaned = cls.clean_header(raw_header)

            for canonical_key, patterns in FIELD_PATTERNS.items():
                if canonical_key in used_canonical:
                    continue

                # Substring check
                if canonical_key in cleaned or any(p.strip("^$") in cleaned for p in patterns[:2]):
                    mappings[raw_header] = canonical_key
                    confidences[canonical_key] = 0.85
                    used_canonical.add(canonical_key)
                    break

        return mappings, confidences

    @classmethod
    def apply_profile(
        cls, headers: List[str], profile: MappingProfile
    ) -> Tuple[Dict[str, str], Dict[str, float]]:
        """Apply a saved mapping profile to input headers."""
        mappings: Dict[str, str] = {}
        confidences: Dict[str, float] = {}

        header_lookup = {cls.clean_header(h): h for h in headers}

        for profile_src, canonical_target in profile.mappings.items():
            cleaned_src = cls.clean_header(profile_src)
            if cleaned_src in header_lookup:
                actual_header = header_lookup[cleaned_src]
                mappings[actual_header] = canonical_target
                confidences[canonical_target] = 1.0

        # Auto-detect remaining unmapped columns
        detected, detected_conf = cls.detect_mappings([h for h in headers if h not in mappings])
        mappings.update(detected)
        confidences.update(detected_conf)

        return mappings, confidences
