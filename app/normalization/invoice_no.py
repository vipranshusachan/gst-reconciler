"""Invoice number normalization and formatting."""

import re

def normalize_invoice_number(raw_invoice_no: str | None) -> str:
    """Normalize invoice number for robust multi-level matching.
    
    Operations:
    1. Strip leading and trailing whitespace.
    2. Convert to uppercase.
    3. Normalize multiple whitespace and separators to single separator or alphanumeric.
    4. Strip non-significant leading zeros in numeric sub-tokens (e.g., 'INV/0042' -> 'INV/42').
    """
    if raw_invoice_no is None:
        return ""
    
    text = str(raw_invoice_no).strip().upper()
    if not text:
        return ""

    # Replace common separators with standard slash '/'
    clean = re.sub(r"[\s\-_\\.]+", "/", text)
    clean = clean.strip("/")

    # Strip leading zeros within numeric segments: e.g. "INV/0042/26" -> "INV/42/26"
    parts = clean.split("/")
    normalized_parts = []
    for part in parts:
        if part.isdigit():
            # Keep at least a single '0' if the number itself is 0
            normalized_parts.append(str(int(part)))
        else:
            # Handle embedded digits e.g. "INV0042" -> "INV42"
            sub_cleaned = re.sub(r"([A-Z]+)0+([1-9][0-9]*)", r"\1\2", part)
            normalized_parts.append(sub_cleaned)

    result = "/".join(normalized_parts)
    return result


def extract_alphanumeric_core(invoice_no: str | None) -> str:
    """Extract strictly alphanumeric characters with leading zeros removed.
    
    Example: 'INV/2026-27/0042' -> 'INV20262742'
    """
    if not invoice_no:
        return ""
    norm = normalize_invoice_number(invoice_no)
    alphanumeric = re.sub(r"[^A-Z0-9]", "", norm)
    return alphanumeric
