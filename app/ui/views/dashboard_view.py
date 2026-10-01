"""Executive Dashboard View displaying high-level KPIs and discrepancy breakdown."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.domain.models import ReconciliationSummary
from app.ui.components.cards import MetricCard


class DashboardView(QWidget):
    """Executive Dashboard with financial summary cards and discrepancy statistics."""

    navigate_to_wizard = Signal()
    load_demo_requested = Signal()
    export_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', sans-serif;
            }
            QTableWidget {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                gridline-color: #334155;
            }
            QHeaderView::section {
                background-color: #334155;
                color: #94a3b8;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
            QPushButton {
                padding: 10px 18px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(20)

        # Header section with action buttons
        hdr_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        lbl_main = QLabel("Reconciliation Dashboard")
        lbl_main.setStyleSheet("font-size: 22px; font-weight: bold; color: #f8fafc;")
        title_box.addWidget(lbl_main)

        self.lbl_subtitle = QLabel("Overview of GST filings vs accounting purchase register")
        self.lbl_subtitle.setStyleSheet("font-size: 12px; color: #94a3b8;")
        title_box.addWidget(self.lbl_subtitle)
        hdr_layout.addLayout(title_box)

        hdr_layout.addStretch()

        btn_demo = QPushButton("Load Demo Data")
        btn_demo.setStyleSheet(
            "background-color: #334155; color: #f8fafc; border: 1px solid #475569;"
        )
        btn_demo.clicked.connect(self.load_demo_requested.emit)
        hdr_layout.addWidget(btn_demo)

        btn_new = QPushButton("+ New Reconciliation")
        btn_new.setStyleSheet("background-color: #3b82f6; color: white;")
        btn_new.clicked.connect(self.navigate_to_wizard.emit)
        hdr_layout.addWidget(btn_new)

        main_layout.addLayout(hdr_layout)

        # Top Metric KPI Cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        self.card_total = MetricCard("Total Invoices", "0", "Awaiting ingestion", "#3b82f6")
        self.card_matched = MetricCard(
            "Matched Rate", "0.0%", "0 matched within tolerance", "#10b981"
        )
        self.card_risk = MetricCard("ITC At Risk", "₹ 0.00", "Missing in GSTR-2B", "#ef4444")
        self.card_diff = MetricCard("Tax Difference", "₹ 0.00", "Net value discrepancy", "#f59e0b")

        cards_layout.addWidget(self.card_total)
        cards_layout.addWidget(self.card_matched)
        cards_layout.addWidget(self.card_risk)
        cards_layout.addWidget(self.card_diff)

        main_layout.addLayout(cards_layout)

        # Discrepancy Breakdown Section
        lbl_breakdown = QLabel("Discrepancy Breakdown & Statutory Impact")
        lbl_breakdown.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #e2e8f0; margin-top: 10px;"
        )
        main_layout.addWidget(lbl_breakdown)

        self.table_breakdown = QTableWidget(5, 4)
        self.table_breakdown.setHorizontalHeaderLabels(
            ["Category", "Invoice Count", "Percentage", "Financial Exposure"]
        )
        self.table_breakdown.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.table_breakdown.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_breakdown.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_breakdown.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.Stretch
        )
        self.table_breakdown.verticalHeader().setVisible(False)
        self.table_breakdown.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        main_layout.addWidget(self.table_breakdown)

    def update_summary(self, summary: ReconciliationSummary):
        """Populate dashboard widgets with latest reconciliation metrics."""
        self.lbl_subtitle.setText(
            f"Project: {summary.project_name} | Reconciled at {summary.created_at}"
        )

        self.card_total.update_values(
            f"{summary.total_processed:,}",
            f"Portal: {summary.total_records_a:,} | Books: {summary.total_records_b:,}",
        )
        self.card_matched.update_values(
            f"{summary.match_rate_percentage:.1f}%",
            f"{summary.total_matched:,} Invoices matched within tolerance",
        )
        self.card_risk.update_values(
            f"₹ {summary.itc_at_risk_amount:,.2f}",
            f"{summary.total_missing_in_a:,} Invoices missing in GSTR-2B",
        )
        self.card_diff.update_values(
            f"₹ {summary.net_diff_tax:,.2f}",
            f"Across {summary.total_matched_with_diff:,} difference records",
        )

        # Update breakdown table rows
        rows = [
            (
                "Matched (Within Configured Tolerance)",
                str(summary.total_matched),
                f"{summary.match_rate_percentage:.1f}%",
                f"₹ {summary.total_taxable_a:,.2f} Taxable Value",
            ),
            (
                "Matched with Monetary Differences",
                str(summary.total_matched_with_diff),
                f"{(summary.total_matched_with_diff / max(summary.total_processed, 1) * 100):.1f}%",
                f"₹ {summary.net_diff_tax:,.2f} Net Delta",
            ),
            (
                "ITC at Risk (Missing in GSTR-2B)",
                str(summary.total_missing_in_a),
                f"{(summary.total_missing_in_a / max(summary.total_processed, 1) * 100):.1f}%",
                f"₹ {summary.itc_at_risk_amount:,.2f} (Action: Follow up with supplier)",
            ),
            (
                "Unclaimed ITC (Missing in Purchase Register)",
                str(summary.total_missing_in_b),
                f"{(summary.total_missing_in_b / max(summary.total_processed, 1) * 100):.1f}%",
                f"₹ {summary.unclaimed_itc_amount:,.2f} (Action: Book in ERP)",
            ),
            (
                "Duplicates in Source Files",
                str(summary.total_duplicates_a + summary.total_duplicates_b),
                "N/A",
                "Potential duplicate payment / excess ITC risk",
            ),
        ]

        for r_idx, row in enumerate(rows):
            for c_idx, val in enumerate(row):
                item = QTableWidgetItem(val)
                if c_idx in (1, 2):
                    item.setTextAlignment(int(Qt.AlignmentFlag.AlignCenter))
                self.table_breakdown.setItem(r_idx, c_idx, item)
