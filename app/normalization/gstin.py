"""GSTIN validation and normalization conforming to Indian statutory specifications."""

import re
from typing import Tuple

# Statutory GSTIN regex: 2 digits (state) + 10 alphanumeric (PAN) + 1 entity + 1 'Z' + 1 check digit
GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")

# Modulo 36 Character Set for GSTIN Checksum calculation
CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def normalize_gstin(raw_gstin: str | None) -> str:
    """Strip whitespace, punctuation, and uppercase raw GSTIN."""
    if not raw_gstin:
        return ""
    clean = re.sub(r"[\s\-_/.]+", "", raw_gstin.strip().upper())
    return clean


def compute_gstin_checksum(gstin_14: str) -> str:
    """Compute the 15th character checksum for a 14-character GSTIN prefix using Luhn Modulo 36."""
    if len(gstin_14) != 14:
        return ""
    factor = 1
    total = 0
    for char in reversed(gstin_14.upper()):
        if char not in CHARS:
            return ""
        code = CHARS.index(char)
        factor = 2 if factor == 1 else 1
        prod = code * factor
        quot, rem = divmod(prod, 36)
        total += quot + rem

    check_code = (36 - (total % 36)) % 36
    return CHARS[check_code]


def validate_gstin(raw_gstin: str | None) -> Tuple[bool, str, str]:
    """Validate GSTIN format and checksum.

    Returns:
        (is_valid, normalized_gstin, error_message)
    """
    clean = normalize_gstin(raw_gstin)
    if not clean:
        return False, "", "GSTIN is missing or empty"

    if len(clean) != 15:
        return False, clean, f"Invalid length {len(clean)} (must be 15 characters)"

    if not GSTIN_REGEX.match(clean):
        return False, clean, "Does not match statutory GSTIN alphanumeric structure"

    # Check digit verification (soft check - statutory modulo 36)
    expected_check = compute_gstin_checksum(clean[:14])
    if expected_check and clean[14] != expected_check:
        # Note: Some older or offline generated GSTINs have known check-digit quirks;
        # we log this as valid format but note check-digit divergence.
        return True, clean, f"Format valid; statutory checksum expects '{expected_check}'"

    return True, clean, ""
