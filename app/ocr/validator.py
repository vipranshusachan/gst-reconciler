"""OCR Text Post-Processing, Field Extraction, and Validation."""

import re
from typing import Dict, Optional

from app.normalization.gstin import normalize_gstin
from app.normalization.invoice_no import normalize_invoice_number

GSTIN_PATTERN = re.compile(r"\b([0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1})\b")
INVOICE_PATTERN = re.compile(
    r"(?:Invoice|Inv|Bill|Voucher)\s*(?:No|Number|#)?[:.\s]*([A-Z0-9\/\-_]+)", re.IGNORECASE
)
DATE_PATTERN = re.compile(
    r"(?:Date)[:.\s]*([0-9]{1,2}[-\/.][0-9]{1,2}[-\/.][0-9]{2,4})", re.IGNORECASE
)
AMOUNT_PATTERN = re.compile(
    r"(?:Taxable|Total|Gross)[:.\s]*(?:Rs\.?|INR|₹)?\s*([0-9,]+\.[0-9]{2})", re.IGNORECASE
)


class OCRFieldExtractor:
    """Extracts structured invoice fields from raw OCR text."""

    @staticmethod
    def extract_fields(ocr_text: str) -> Dict[str, Optional[str]]:
        results: Dict[str, Optional[str]] = {
            "supplier_gstin": None,
            "invoice_number": None,
            "invoice_date": None,
            "taxable_value": None,
            "total_invoice_value": None,
        }

        # Find GSTIN
        gstin_match = GSTIN_PATTERN.search(ocr_text)
        if gstin_match:
            results["supplier_gstin"] = normalize_gstin(gstin_match.group(1))

        # Find Invoice Number
        inv_match = INVOICE_PATTERN.search(ocr_text)
        if inv_match:
            results["invoice_number"] = normalize_invoice_number(inv_match.group(1))

        # Find Date
        date_match = DATE_PATTERN.search(ocr_text)
        if date_match:
            results["invoice_date"] = date_match.group(1)

        # Find Amounts
        amt_matches = AMOUNT_PATTERN.findall(ocr_text)
        if amt_matches:
            # Clean commas
            cleaned_amts = [re.sub(r"[^\d.]", "", a) for a in amt_matches]
            if len(cleaned_amts) >= 1:
                results["taxable_value"] = cleaned_amts[0]
            if len(cleaned_amts) >= 2:
                results["total_invoice_value"] = cleaned_amts[1]

        return results
