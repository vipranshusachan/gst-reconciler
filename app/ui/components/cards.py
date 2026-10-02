"""Reusable UI Card Widgets for Dashboard and Executive Metrics."""

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class MetricCard(QFrame):
    """Clean, high-contrast KPI card displaying a primary metric, label, and explanation."""

    def __init__(
        self,
        title: str,
        value: str,
        subtitle: str = "",
        highlight_color: str = "#2563eb",
        parent=None,
    ):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-left: 5px solid {highlight_color};
                border-radius: 10px;
                padding: 14px 16px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        # Title Label
        self.lbl_title = QLabel(title.upper())
        self.lbl_title.setStyleSheet(
            "color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 0.8px; border: none; background: transparent;"
        )
        layout.addWidget(self.lbl_title)

        # Primary Metric Value
        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(
            "color: #0f172a; font-size: 24px; font-weight: 800; border: none; background: transparent;"
        )
        layout.addWidget(self.lbl_value)

        # Explanatory Subtitle
        self.lbl_sub = QLabel(subtitle)
        self.lbl_sub.setWordWrap(True)
        self.lbl_sub.setStyleSheet(
            "color: #475569; font-size: 12px; font-weight: 500; border: none; background: transparent;"
        )
        layout.addWidget(self.lbl_sub)

    def update_values(self, value: str, subtitle: str = ""):
        self.lbl_value.setText(value)
        if subtitle:
            self.lbl_sub.setText(subtitle)
