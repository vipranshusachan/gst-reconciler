"""Unit tests for invoice number normalization and token extraction."""

from app.normalization.invoice_no import extract_alphanumeric_core, normalize_invoice_number

def test_normalize_invoice_number():
    assert normalize_invoice_number("  inv/2026/0042  ") == "INV/2026/42"
    assert normalize_invoice_number("INV-0001") == "INV/1"
    assert normalize_invoice_number("bill 99") == "BILL/99"
    assert normalize_invoice_number(None) == ""
    assert normalize_invoice_number("") == ""


def test_extract_alphanumeric_core():
    assert extract_alphanumeric_core("INV/2026-27/0042") == "INV20262742"
    assert extract_alphanumeric_core("DOC-0091") == "DOC91"
    assert extract_alphanumeric_core(None) == ""
