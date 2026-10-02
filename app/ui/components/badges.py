"""Status Badges and Color Helpers for Reconciliation States."""

from PySide6.QtWidgets import QLabel

from app.domain.enums import MatchStatus

STATUS_COLORS = {
    MatchStatus.MATCHED: ("#047857", "#d1fae5", "#a7f3d0"),  # Text, bg, border
    MatchStatus.MATCHED_WITH_DIFFERENCE: ("#b45309", "#fef3c7", "#fde68a"),
    MatchStatus.MISSING_IN_SOURCE_A: (
        "#b91c1c",
        "#fee2e2",
        "#fca5a5",
    ),  # Missing in 2B (ITC At Risk)
    MatchStatus.MISSING_IN_SOURCE_B: ("#6d28d9", "#ede9fe", "#ddd6fe"),  # Unclaimed in books
    MatchStatus.DUPLICATE: ("#be123c", "#ffe4e6", "#fecdd3"),
    MatchStatus.INVALID_DATA: ("#475569", "#f1f5f9", "#cbd5e1"),
}

STATUS_LABELS = {
    MatchStatus.MATCHED: "✓ MATCHED",
    MatchStatus.MATCHED_WITH_DIFFERENCE: "⚠ TAX DIFF",
    MatchStatus.MISSING_IN_SOURCE_A: "✕ MISSING IN 2B (RISK)",
    MatchStatus.MISSING_IN_SOURCE_B: "★ UNCLAIMED IN BOOKS",
    MatchStatus.DUPLICATE: "⚠ DUPLICATE",
    MatchStatus.INVALID_DATA: "✕ INVALID",
}


def create_status_badge(status: MatchStatus) -> QLabel:
    """Return a styled QLabel formatted as a status pill badge."""
    text_color, bg_color, border_color = STATUS_COLORS.get(
        status, ("#334155", "#f1f5f9", "#cbd5e1")
    )
    label_text = STATUS_LABELS.get(status, status.value)

    badge = QLabel(f" {label_text} ")
    badge.setStyleSheet(f"""
        QLabel {{
            color: {text_color};
            background-color: {bg_color};
            border: 1px solid {border_color};
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
        }}
    """)
    return badge
