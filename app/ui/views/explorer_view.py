"""Issue Explorer View for browsing, filtering, and investigating reconciled records."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from app.domain.enums import MatchStatus
from app.domain.models import ReconciliationSummary
from app.ui.models.table_model import ReconciledTableModel
from app.ui.views.comparison_dialog import ComparisonDialog


class IssueExplorerView(QWidget):
    """High-density data grid for exploring issues and manual audit resolution."""

    review_updated = Signal(str, str, str)  # match_id, new_status, note

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 8px 12px;
                color: #f8fafc;
                font-size: 13px;
            }
            QTableView {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                gridline-color: #334155;
                selection-background-color: #3b82f6;
            }
            QHeaderView::section {
                background-color: #334155;
                color: #94a3b8;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
            QPushButton {
                padding: 6px 14px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 20, 28, 20)
        layout.setSpacing(14)

        # Header Title
        hdr_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        lbl_title = QLabel("Issue Explorer & Discrepancy Ledger")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f8fafc;")
        title_box.addWidget(lbl_title)

        self.lbl_count = QLabel("0 records loaded")
        self.lbl_count.setStyleSheet("font-size: 12px; color: #94a3b8;")
        title_box.addWidget(self.lbl_count)
        hdr_layout.addLayout(title_box)

        hdr_layout.addStretch()

        # Search Bar
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Search GSTIN, Supplier Name, or Invoice #...")
        self.txt_search.setFixedWidth(320)
        self.txt_search.textChanged.connect(self._on_filter_changed)
        hdr_layout.addWidget(self.txt_search)

        layout.addLayout(hdr_layout)

        # Filter Pills Bar
        pill_layout = QHBoxLayout()
        pill_layout.setSpacing(8)
        self.btn_group = QButtonGroup(self)

        filters = [
            ("All Records", "ALL"),
            ("Matched", MatchStatus.MATCHED.value),
            ("Differences", MatchStatus.MATCHED_WITH_DIFFERENCE.value),
            ("Missing in 2B (Risk)", MatchStatus.MISSING_IN_SOURCE_A.value),
            ("Unclaimed in Books", MatchStatus.MISSING_IN_SOURCE_B.value),
            ("Duplicates", MatchStatus.DUPLICATE.value),
        ]

        self.current_filter = "ALL"
        for idx, (label, code) in enumerate(filters):
            btn = QPushButton(label)
            btn.setCheckable(True)
            if idx == 0:
                btn.setChecked(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1e293b;
                    color: #94a3b8;
                    border: 1px solid #334155;
                }
                QPushButton:checked {
                    background-color: #3b82f6;
                    color: white;
                    border: 1px solid #3b82f6;
                }
            """)
            btn.clicked.connect(lambda checked, c=code: self._set_filter(c))
            self.btn_group.addButton(btn)
            pill_layout.addWidget(btn)

        pill_layout.addStretch()
        layout.addLayout(pill_layout)

        # Table Grid
        self.table_model = ReconciledTableModel()
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_view.horizontalHeader().setSectionResizeMode(14, QHeaderView.ResizeMode.Stretch)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table_view.doubleClicked.connect(self._on_row_double_clicked)

        layout.addWidget(self.table_view)

        # Bottom Hint Bar
        hint = QLabel(
            "💡 Tip: Double-click any row to view Side-by-Side invoice field comparison and take resolution action."
        )
        hint.setStyleSheet("color: #64748b; font-size: 11px;")
        layout.addWidget(hint)

    def load_summary(self, summary: ReconciliationSummary):
        self.table_model.set_records(summary.matches)
        self._update_count_label()

    def _set_filter(self, filter_code: str):
        self.current_filter = filter_code
        self._on_filter_changed()

    def _on_filter_changed(self):
        query = self.txt_search.text()
        self.table_model.filter(self.current_filter, query)
        self._update_count_label()

    def _update_count_label(self):
        total = len(self.table_model._all_records)
        shown = len(self.table_model._filtered_records)
        self.lbl_count.setText(f"Showing {shown} of {total} records")

    def _on_row_double_clicked(self, index):
        rec = self.table_model.get_record(index.row())
        if rec:
            dlg = ComparisonDialog(rec, self)
            dlg.review_updated.connect(self._on_review_updated)
            dlg.exec()

    def _on_review_updated(self, match_id: str, new_status: str, note: str):
        self.table_model.filter(self.current_filter, self.txt_search.text())
        self.review_updated.emit(match_id, new_status, note)
