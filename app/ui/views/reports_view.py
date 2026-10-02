"""Reports and Export View."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.application.service import ReconciliationService
from app.domain.models import ReconciliationSummary


class ReportsView(QWidget):
    """Export hub for Excel workbooks and CSV files."""

    def __init__(self, service: ReconciliationService, parent=None):
        super().__init__(parent)
        self.service = service
        self.current_summary: Optional[ReconciliationSummary] = None

        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                color: #0f172a;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            }
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 20px;
            }
            QPushButton {
                padding: 11px 22px;
                border-radius: 6px;
                font-weight: 700;
                font-size: 13px;
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(20)

        # Header
        lbl_title = QLabel("Audit Reports & Data Export")
        lbl_title.setStyleSheet("font-size: 22px; font-weight: 800; color: #0f172a;")
        layout.addWidget(lbl_title)

        desc = QLabel(
            "Download audit-ready spreadsheets for filing, supplier communication, and internal accounting records."
        )
        desc.setStyleSheet("color: #64748b; font-size: 13px; font-weight: 500;")
        layout.addWidget(desc)

        # Excel Export Card
        card_excel = QFrame()
        lay_ex = QVBoxLayout(card_excel)
        lay_ex.setSpacing(10)
        lbl_ex_hdr = QLabel("📊  <b>Complete GST Audit Workbook (.xlsx)</b>")
        lbl_ex_hdr.setStyleSheet("font-size: 15px; color: #0f172a;")
        lay_ex.addWidget(lbl_ex_hdr)

        lbl_ex_desc = QLabel(
            "Multi-tab Excel workbook formatted for CAs and Tax Auditors. Contains dedicated sheets for: "
            "<b>Executive Summary, Matched Invoices, Tax Discrepancies, ITC at Risk (for supplier follow-up), and Unclaimed Invoices (for Tally entry).</b>"
        )
        lbl_ex_desc.setStyleSheet("color: #475569; font-size: 12px; line-height: 1.4;")
        lbl_ex_desc.setWordWrap(True)
        lay_ex.addWidget(lbl_ex_desc)

        btn_excel = QPushButton("Export Multi-Tab Excel Report 📊")
        btn_excel.setStyleSheet("""
            QPushButton {
                background-color: #16a34a;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #15803d;
            }
        """)
        btn_excel.clicked.connect(self._export_excel)
        lay_ex.addWidget(btn_excel)
        layout.addWidget(card_excel)

        # CSV Export Card
        card_csv = QFrame()
        lay_csv = QVBoxLayout(card_csv)
        lay_csv.setSpacing(10)
        lbl_csv_hdr = QLabel("📄  <b>Raw Reconciled Ledger (.csv)</b>")
        lbl_csv_hdr.setStyleSheet("font-size: 15px; color: #0f172a;")
        lay_csv.addWidget(lbl_csv_hdr)

        lbl_csv_desc = QLabel(
            "Standard tabular CSV file containing every reconciled invoice, match confidence score, delta amounts, and audit notes. "
            "Ideal for importing directly into custom ERP databases or reporting software."
        )
        lbl_csv_desc.setStyleSheet("color: #475569; font-size: 12px; line-height: 1.4;")
        lbl_csv_desc.setWordWrap(True)
        lay_csv.addWidget(lbl_csv_desc)

        btn_csv = QPushButton("Export Reconciled CSV File 📄")
        btn_csv.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        btn_csv.clicked.connect(self._export_csv)
        lay_csv.addWidget(btn_csv)
        layout.addWidget(card_csv)

        layout.addStretch()

    def set_summary(self, summary: ReconciliationSummary):
        self.current_summary = summary

    def _export_excel(self):
        if not self.current_summary:
            QMessageBox.warning(self, "No Data", "Please run or load a reconciliation first.")
            return

        default_name = f"GST_Audit_Report_{Path(self.current_summary.source_b_file).stem}.xlsx"
        path_str, _ = QFileDialog.getSaveFileName(
            self, "Save Excel Report", default_name, "Excel Files (*.xlsx)"
        )
        if not path_str:
            return

        try:
            self.service.export_excel(self.current_summary, Path(path_str))
            QMessageBox.information(
                self, "Success", f"Excel report generated successfully:\n{path_str}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export Excel report: {e}")

    def _export_csv(self):
        if not self.current_summary:
            QMessageBox.warning(self, "No Data", "Please run or load a reconciliation first.")
            return

        default_name = f"GST_Reconciliation_{Path(self.current_summary.source_b_file).stem}.csv"
        path_str, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", default_name, "CSV Files (*.csv)"
        )
        if not path_str:
            return

        try:
            self.service.export_csv(self.current_summary, Path(path_str))
            QMessageBox.information(self, "Success", f"CSV file exported successfully:\n{path_str}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export CSV: {e}")
