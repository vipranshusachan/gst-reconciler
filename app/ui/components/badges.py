"""Status Badges and Color Helpers for Reconciliation States."""

from PySide6.QtWidgets import QLabel

from app.domain.enums import MatchStatus

STATUS_COLORS = {
    MatchStatus.MATCHED: ("#065f46", "#d1fae5"),  # Dark green on soft mint
    MatchStatus.MATCHED_WITH_DIFFERENCE: ("#92400e", "#fef3c7"),  # Dark amber on soft yellow
    MatchStatus.MISSING_IN_SOURCE_A: ("#991b1b", "#fee2e2"),  # Dark red on soft pink
    MatchStatus.MISSING_IN_SOURCE_B: ("#5b21b6", "#ede9fe"),  # Dark purple on soft lavender
    MatchStatus.DUPLICATE: ("#831843", "#fce7f3"),  # Dark rose on soft rose
    MatchStatus.INVALID_DATA: ("#374151", "#f3f4f6"),  # Dark gray
}

STATUS_LABELS = {
    MatchStatus.MATCHED: "MATCHED",
    MatchStatus.MATCHED_WITH_DIFFERENCE: "DIFFERENCE",
    MatchStatus.MISSING_IN_SOURCE_A: "MISSING IN 2B",
    MatchStatus.MISSING_IN_SOURCE_B: "UNCLAIMED",
    MatchStatus.DUPLICATE: "DUPLICATE",
    MatchStatus.INVALID_DATA: "INVALID",
}


def create_status_badge(status: MatchStatus) -> QLabel:
    """Return a styled QLabel formatted as a status pill badge."""
    text_color, bg_color = STATUS_COLORS.get(status, ("#ffffff", "#475569"))
    label_text = STATUS_LABELS.get(status, status.value)

    badge = QLabel(f" {label_text} ")
    badge.setStyleSheet(f"""
        QLabel {{
            color: {text_color};
            background-color: {bg_color};
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            padding: 3px 6px;
        }}
    """)
    return badge
