"""Reports and Export View."""

from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
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
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', sans-serif;
            }
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 20px;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(20)

        # Header
        lbl_title = QLabel("Audit Reports & Data Export")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f8fafc;")
        layout.addWidget(lbl_title)

        desc = QLabel("Generate audit-ready spreadsheets and data pipelines from the latest reconciliation run.")
        desc.setStyleSheet("color: #94a3b8; font-size: 13px;")
        layout.addWidget(desc)

        # Excel Export Card
        card_excel = QFrame()
        lay_ex = QVBoxLayout(card_excel)
        lay_ex.addWidget(QLabel("<b>Excel Audit Workbook (.xlsx)</b>"))
        lbl_ex_desc = QLabel("Comprehensive multi-tab Excel file containing Executive Summary, Itemized Mismatches, ITC at Risk, Unclaimed ITC, and Matched sheets with financial color tags.")
        lbl_ex_desc.setStyleSheet("color: #94a3b8; font-size: 12px;")
        lbl_ex_desc.setWordWrap(True)
        lay_ex.addWidget(lbl_ex_desc)

        btn_excel = QPushButton("Export Formatted Excel Report 📊")
        btn_excel.setStyleSheet("background-color: #10b981; color: white;")
        btn_excel.clicked.connect(self._export_excel)
        lay_ex.addWidget(btn_excel)
        layout.addWidget(card_excel)

        # CSV Export Card
        card_csv = QFrame()
        lay_csv = QVBoxLayout(card_csv)
        lay_csv.addWidget(QLabel("<b>Raw Reconciled Ledger (.csv)</b>"))
        lbl_csv_desc = QLabel("Flat CSV format for importing into ERPs, custom business intelligence pipelines, or database ingestion.")
        lbl_csv_desc.setStyleSheet("color: #94a3b8; font-size: 12px;")
        lbl_csv_desc.setWordWrap(True)
        lay_csv.addWidget(lbl_csv_desc)

        btn_csv = QPushButton("Export Flat CSV File 📄")
        btn_csv.setStyleSheet("background-color: #3b82f6; color: white;")
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
        path_str, _ = QFileDialog.getSaveFileName(self, "Save Excel Report", default_name, "Excel Files (*.xlsx)")
        if not path_str:
            return

        try:
            self.service.export_excel(self.current_summary, Path(path_str))
            QMessageBox.information(self, "Success", f"Excel report generated successfully:\n{path_str}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export Excel report: {e}")

    def _export_csv(self):
        if not self.current_summary:
            QMessageBox.warning(self, "No Data", "Please run or load a reconciliation first.")
            return

        default_name = f"GST_Reconciliation_{Path(self.current_summary.source_b_file).stem}.csv"
        path_str, _ = QFileDialog.getSaveFileName(self, "Save CSV File", default_name, "CSV Files (*.csv)")
        if not path_str:
            return

        try:
            self.service.export_csv(self.current_summary, Path(path_str))
            QMessageBox.information(self, "Success", f"CSV file exported successfully:\n{path_str}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export CSV: {e}")
