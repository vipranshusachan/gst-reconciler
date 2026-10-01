"""Reusable UI Card Widgets for Dashboard and Executive Metrics."""

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class MetricCard(QFrame):
    """Sleek KPI card displaying a primary value, title, and auxiliary subtitle."""

    def __init__(
        self,
        title: str,
        value: str,
        subtitle: str = "",
        highlight_color: str = "#3b82f6",
        parent=None,
    ):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #1e293b;
                border: 1px solid #334155;
                border-left: 4px solid {highlight_color};
                border-radius: 8px;
                padding: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        # Title
        self.lbl_title = QLabel(title.upper())
        self.lbl_title.setStyleSheet(
            "color: #94a3b8; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;"
        )
        layout.addWidget(self.lbl_title)

        # Primary Metric Value
        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet("color: #f8fafc; font-size: 22px; font-weight: bold;")
        layout.addWidget(self.lbl_value)

        # Subtitle
        self.lbl_sub = QLabel(subtitle)
        self.lbl_sub.setStyleSheet("color: #64748b; font-size: 11px;")
        layout.addWidget(self.lbl_sub)

    def update_values(self, value: str, subtitle: str = ""):
        self.lbl_value.setText(value)
        if subtitle:
            self.lbl_sub.setText(subtitle)
