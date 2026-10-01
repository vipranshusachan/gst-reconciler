"""Unit tests for GSTIN normalization and checksum validation."""

import pytest
from app.normalization.gstin import compute_gstin_checksum, normalize_gstin, validate_gstin

def test_normalize_gstin():
    assert normalize_gstin("  27aabct3518q1z6  ") == "27AABCT3518Q1Z6"
    assert normalize_gstin("27-AABCT3518Q1Z6") == "27AABCT3518Q1Z6"
    assert normalize_gstin(None) == ""


def test_validate_valid_gstin():
    valid_gstin = "27AABCT3518Q1Z6"
    is_valid, clean, err = validate_gstin(valid_gstin)
    assert is_valid is True
    assert clean == "27AABCT3518Q1Z6"


def test_validate_invalid_gstin_length():
    is_valid, clean, err = validate_gstin("27AABCT3518Q1Z")  # 14 chars
    assert is_valid is False
    assert "Invalid length" in err


def test_validate_invalid_gstin_structure():
    is_valid, clean, err = validate_gstin("2712345678Q1Z6A")  # numeric PAN
    assert is_valid is False
    assert "alphanumeric structure" in err


def test_compute_checksum():
    chk = compute_gstin_checksum("27AABCT3518Q1Z")
    assert isinstance(chk, str)
    assert len(chk) == 1
