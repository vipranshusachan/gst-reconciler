"""Side-by-Side Comparison Modal Dialog for Deep Invoice Inspection."""

from decimal import Decimal
from typing import Optional
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from app.domain.enums import ReviewStatus
from app.domain.models import MatchRecord

class ComparisonDialog(QDialog):
    """Side-by-side inspection dialog showing field deltas and review actions."""

    review_updated = Signal(str, str, str)  # match_id, new_status, note

    def __init__(self, match: MatchRecord, parent=None):
        super().__init__(parent)
        self.match = match
        self.setWindowTitle(f"Invoice Comparison — {match.match_id[:8]}")
        self.resize(800, 550)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #f8fafc;
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Header with status & reason
        hdr_frame = QFrame()
        hdr_frame.setStyleSheet("background-color: #1e293b; border-radius: 8px; padding: 12px;")
        hdr_layout = QVBoxLayout(hdr_frame)
        
        status_lbl = QLabel(f"Match Status: {match.match_status.value} (Level: {match.match_level.value})")
        status_lbl.setStyleSheet("color: #38bdf8; font-size: 15px; font-weight: bold;")
        hdr_layout.addWidget(status_lbl)

        explanation_lbl = QLabel(match.explanation)
        explanation_lbl.setStyleSheet("color: #cbd5e1; font-size: 12px;")
        explanation_lbl.setWordWrap(True)
        hdr_layout.addWidget(explanation_lbl)

        layout.addWidget(hdr_frame)

        # Side-by-side grid
        grid_frame = QFrame()
        grid_frame.setStyleSheet("background-color: #1e293b; border-radius: 8px; padding: 16px;")
        grid = QGridLayout(grid_frame)
        grid.setSpacing(10)

        # Table Column Headers
        col_field = QLabel("ATTRIBUTE")
        col_field.setStyleSheet("color: #94a3b8; font-weight: bold; font-size: 11px;")
        col_a = QLabel("SOURCE A (PORTAL GSTR-2B)")
        col_a.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 11px;")
        col_b = QLabel("SOURCE B (PURCHASE REGISTER)")
        col_b.setStyleSheet("color: #a78bfa; font-weight: bold; font-size: 11px;")
        col_diff = QLabel("DIFFERENCE (DELTA)")
        col_diff.setStyleSheet("color: #fbbf24; font-weight: bold; font-size: 11px;")

        grid.addWidget(col_field, 0, 0)
        grid.addWidget(col_a, 0, 1)
        grid.addWidget(col_b, 0, 2)
        grid.addWidget(col_diff, 0, 3)

        ra = match.record_a
        rb = match.record_b

        fields = [
            ("Supplier GSTIN", ra.supplier_gstin if ra else "-", rb.supplier_gstin if rb else "-", "MATCH" if (ra and rb and ra.supplier_gstin == rb.supplier_gstin) else "DIFF"),
            ("Supplier Name", ra.supplier_name if (ra and ra.supplier_name) else "-", rb.supplier_name if (rb and rb.supplier_name) else "-", "-"),
            ("Invoice Number", ra.raw_invoice_number if ra else "-", rb.raw_invoice_number if rb else "-", "MATCH" if (ra and rb and ra.raw_invoice_number == rb.raw_invoice_number) else "DIFF"),
            ("Invoice Date", ra.invoice_date.isoformat() if (ra and ra.invoice_date) else "-", rb.invoice_date.isoformat() if (rb and rb.invoice_date) else "-", "-"),
            ("Taxable Value", f"₹ {ra.taxable_value:,.2f}" if ra else "-", f"₹ {rb.taxable_value:,.2f}" if rb else "-", f"{match.diff_taxable:+,.2f}"),
            ("IGST Amount", f"₹ {ra.igst:,.2f}" if ra else "-", f"₹ {rb.igst:,.2f}" if rb else "-", f"{match.diff_igst:+,.2f}"),
            ("CGST Amount", f"₹ {ra.cgst:,.2f}" if ra else "-", f"₹ {rb.cgst:,.2f}" if rb else "-", f"{match.diff_cgst:+,.2f}"),
            ("SGST Amount", f"₹ {ra.sgst:,.2f}" if ra else "-", f"₹ {rb.sgst:,.2f}" if rb else "-", f"{match.diff_sgst:+,.2f}"),
            ("Total Tax", f"₹ {ra.calculate_total_tax():,.2f}" if ra else "-", f"₹ {rb.calculate_total_tax():,.2f}" if rb else "-", f"{match.diff_total_tax:+,.2f}"),
            ("Total Invoice Value", f"₹ {ra.total_invoice_value:,.2f}" if ra else "-", f"₹ {rb.total_invoice_value:,.2f}" if rb else "-", f"{match.diff_total_value:+,.2f}"),
        ]

        for row_idx, (f_name, val_a, val_b, delta) in enumerate(fields, 1):
            lbl_f = QLabel(f_name)
            lbl_f.setStyleSheet("color: #94a3b8; font-weight: 500;")
            lbl_a = QLabel(val_a)
            lbl_a.setStyleSheet("color: #f8fafc; font-family: monospace;")
            lbl_b = QLabel(val_b)
            lbl_b.setStyleSheet("color: #f8fafc; font-family: monospace;")
            lbl_d = QLabel(delta)
            
            # Highlight differences
            if delta != "-" and delta != "MATCH" and delta != "+0.00" and delta != "0.00":
                lbl_d.setStyleSheet("color: #f59e0b; font-weight: bold; font-family: monospace;")
            else:
                lbl_d.setStyleSheet("color: #64748b; font-family: monospace;")

            grid.addWidget(lbl_f, row_idx, 0)
            grid.addWidget(lbl_a, row_idx, 1)
            grid.addWidget(lbl_b, row_idx, 2)
            grid.addWidget(lbl_d, row_idx, 3)

        layout.addWidget(grid_frame)

        # Review & Resolution Action Bar
        act_frame = QFrame()
        act_layout = QHBoxLayout(act_frame)
        act_layout.setContentsMargins(0, 0, 0, 0)

        self.txt_note = QLineEdit()
        self.txt_note.setPlaceholderText("Optional review note (e.g. Approved round-off tolerance)...")
        self.txt_note.setStyleSheet("background-color: #1e293b; color: #f8fafc; border: 1px solid #334155; border-radius: 6px; padding: 8px;")
        act_layout.addWidget(self.txt_note)

        btn_accept = QPushButton("Accept Difference")
        btn_accept.setStyleSheet("background-color: #10b981; color: white;")
        btn_accept.clicked.connect(lambda: self._set_review(ReviewStatus.ACCEPTED))
        act_layout.addWidget(btn_accept)

        btn_reject = QPushButton("Reject / Mark Vendor Error")
        btn_reject.setStyleSheet("background-color: #ef4444; color: white;")
        btn_reject.clicked.connect(lambda: self._set_review(ReviewStatus.REJECTED))
        act_layout.addWidget(btn_reject)

        btn_close = QPushButton("Close")
        btn_close.setStyleSheet("background-color: #475569; color: white;")
        btn_close.clicked.connect(self.accept)
        act_layout.addWidget(btn_close)

        layout.addWidget(act_frame)

    def _set_review(self, status: ReviewStatus):
        self.match.review_status = status
        self.match.review_note = self.txt_note.text()
        self.review_updated.emit(self.match.match_id, status.value, self.match.review_note)
        self.accept()
