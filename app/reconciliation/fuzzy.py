"""Fuzzy string comparison module with RapidFuzz and pure-Python fallback."""

import difflib
from typing import Tuple

try:
    from rapidfuzz import fuzz

    HAS_RAPIDFUZZ = True
except ImportError:
    HAS_RAPIDFUZZ = False


def compute_string_similarity(str1: str, str2: str) -> float:
    """Compute similarity ratio between 0.0 and 1.0 using Token Sort / Levenshtein.

    Case-insensitive and whitespace-tolerant.
    """
    if not str1 or not str2:
        return 0.0

    s1 = str1.strip().upper()
    s2 = str2.strip().upper()

    if s1 == s2:
        return 1.0

    if HAS_RAPIDFUZZ:
        # RapidFuzz token sort ratio
        ratio = fuzz.token_sort_ratio(s1, s2) / 100.0
        return float(ratio)
    else:
        # Standard library difflib fallback
        # Token sort simulation
        tokens1 = " ".join(sorted(s1.split()))
        tokens2 = " ".join(sorted(s2.split()))
        return difflib.SequenceMatcher(None, tokens1, tokens2).ratio()


def is_fuzzy_match(inv1: str, inv2: str, threshold: float = 0.85) -> Tuple[bool, float]:
    """Determine if two invoice strings match under fuzzy threshold."""
    score = compute_string_similarity(inv1, inv2)
    return (score >= threshold, score)
