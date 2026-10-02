"""Executive Dashboard View displaying high-level KPIs and discrepancy breakdown."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
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
    """Executive Dashboard with financial summary cards, guidance banner, and discrepancy statistics."""

    navigate_to_wizard = Signal()
    load_demo_requested = Signal()
    export_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                color: #0f172a;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            }
            QTableWidget {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #f1f5f9;
                font-size: 13px;
                selection-background-color: #eff6ff;
                selection-color: #1e40af;
            }
            QHeaderView::section {
                background-color: #f1f5f9;
                color: #334155;
                font-weight: 700;
                font-size: 12px;
                padding: 10px 12px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
            }
            QPushButton {
                padding: 10px 18px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 28, 32, 28)
        main_layout.setSpacing(20)

        # Header section with action buttons
        hdr_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(4)
        lbl_main = QLabel("Reconciliation Dashboard")
        lbl_main.setStyleSheet("font-size: 24px; font-weight: 800; color: #0f172a;")
        title_box.addWidget(lbl_main)

        self.lbl_subtitle = QLabel(
            "Overview of GST Portal Return (GSTR-2B) vs Accounting Purchase Register"
        )
        self.lbl_subtitle.setStyleSheet("font-size: 13px; color: #64748b; font-weight: 500;")
        title_box.addWidget(self.lbl_subtitle)
        hdr_layout.addLayout(title_box)

        hdr_layout.addStretch()

        btn_demo = QPushButton("📂  Load Sample Demo")
        btn_demo.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #334155;
                border: 1px solid #cbd5e1;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
                border-color: #94a3b8;
            }
        """)
        btn_demo.clicked.connect(self.load_demo_requested.emit)
        hdr_layout.addWidget(btn_demo)

        btn_new = QPushButton("+ New Reconciliation")
        btn_new.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        btn_new.clicked.connect(self.navigate_to_wizard.emit)
        hdr_layout.addWidget(btn_new)

        main_layout.addLayout(hdr_layout)

        # Top Metric KPI Cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        self.card_total = MetricCard("TOTAL INVOICES", "0", "Upload files to start", "#2563eb")
        self.card_matched = MetricCard(
            "SAFE TO CLAIM (MATCHED)", "0.0%", "0 matched within tolerance", "#16a34a"
        )
        self.card_risk = MetricCard(
            "ITC AT RISK", "₹ 0.00", "Missing in GSTR-2B (Action required)", "#dc2626"
        )
        self.card_diff = MetricCard(
            "TAX DIFFERENCE", "₹ 0.00", "Net value or rate variance", "#d97706"
        )

        cards_layout.addWidget(self.card_total)
        cards_layout.addWidget(self.card_matched)
        cards_layout.addWidget(self.card_risk)
        cards_layout.addWidget(self.card_diff)

        main_layout.addLayout(cards_layout)

        # Accountant Guidance / Statutory Action Banner
        guide_box = QFrame()
        guide_box.setStyleSheet("""
            QFrame {
                background-color: #eff6ff;
                border: 1px solid #bfdbfe;
                border-left: 5px solid #3b82f6;
                border-radius: 8px;
                padding: 12px 16px;
            }
        """)
        g_lay = QVBoxLayout(guide_box)
        g_lay.setContentsMargins(12, 10, 12, 10)
        g_lay.setSpacing(6)

        g_title = QLabel("💡 <b>Quick Tax & Statutory Guidance for Accountants:</b>")
        g_title.setStyleSheet(
            "color: #1e40af; font-size: 13px; font-weight: 700; background: transparent; border: none;"
        )
        g_lay.addWidget(g_title)

        g_desc = QLabel(
            "• <b>Matched Invoices:</b> Validated for 100% safe Input Tax Credit (ITC) claim in GSTR-3B.<br>"
            "• <b>ITC at Risk:</b> Supplier hasn't filed GSTR-1. Withhold tax payment or notify vendor immediately to avoid tax penalties.<br>"
            "• <b>Unclaimed ITC:</b> Present on GST portal but missing in your books. Book these invoices in Tally/ERP to claim additional credit."
        )
        g_desc.setStyleSheet(
            "color: #1e3a8a; font-size: 12px; line-height: 1.4; background: transparent; border: none;"
        )
        g_desc.setWordWrap(True)
        g_lay.addWidget(g_desc)
        main_layout.addWidget(guide_box)

        # Discrepancy Breakdown Section
        lbl_breakdown = QLabel("Audit Breakdown & Action Ledger")
        lbl_breakdown.setStyleSheet(
            "font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 6px;"
        )
        main_layout.addWidget(lbl_breakdown)

        self.table_breakdown = QTableWidget(5, 4)
        self.table_breakdown.setHorizontalHeaderLabels(
            ["Category & Action", "Invoice Count", "% Share", "Statutory Impact / Total Value"]
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

        # Update breakdown table rows with clear accountant-friendly descriptions
        rows = [
            (
                "✓ Safe ITC: Matched within tolerance",
                str(summary.total_matched),
                f"{summary.match_rate_percentage:.1f}%",
                f"₹ {summary.total_taxable_a:,.2f} Taxable Value (Ready for GSTR-3B)",
            ),
            (
                "⚠ Tax Discrepancy: Difference in amounts",
                str(summary.total_matched_with_diff),
                f"{(summary.total_matched_with_diff / max(summary.total_processed, 1) * 100):.1f}%",
                f"₹ {summary.net_diff_tax:,.2f} Net Variance (Review difference)",
            ),
            (
                "✕ ITC at Risk: Missing in Portal (GSTR-2B)",
                str(summary.total_missing_in_a),
                f"{(summary.total_missing_in_a / max(summary.total_processed, 1) * 100):.1f}%",
                f"₹ {summary.itc_at_risk_amount:,.2f} (Action: Follow up with supplier)",
            ),
            (
                "★ Unclaimed ITC: In Portal but Missing in Books",
                str(summary.total_missing_in_b),
                f"{(summary.total_missing_in_b / max(summary.total_processed, 1) * 100):.1f}%",
                f"₹ {summary.unclaimed_itc_amount:,.2f} (Action: Book in Tally/ERP)",
            ),
            (
                "⚠ Duplicate Invoices Detected",
                str(summary.total_duplicates_a + summary.total_duplicates_b),
                "N/A",
                "Review to prevent duplicate payment or wrongful claim",
            ),
        ]

        for r_idx, row in enumerate(rows):
            for c_idx, val in enumerate(row):
                item = QTableWidgetItem(val)
                if c_idx in (1, 2):
                    item.setTextAlignment(int(Qt.AlignmentFlag.AlignCenter))
                self.table_breakdown.setItem(r_idx, c_idx, item)
