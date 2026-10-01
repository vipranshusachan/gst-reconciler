"""Virtualized QAbstractTableModel for High-Performance Match Records Grid."""

from decimal import Decimal
from typing import Any, List, Optional
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtGui import QColor

from app.domain.enums import MatchStatus
from app.domain.models import MatchRecord

COLUMNS = [
    "Status",
    "Supplier GSTIN",
    "Supplier Name",
    "Portal Inv #",
    "Books Inv #",
    "Invoice Date",
    "Match Level",
    "Taxable (2B)",
    "Taxable (Books)",
    "Diff Taxable",
    "Tax (2B)",
    "Tax (Books)",
    "Diff Tax",
    "Review",
    "Explanation",
]

class ReconciledTableModel(QAbstractTableModel):
    """Virtualized table model supporting 100k+ rows with sorting and filtering."""

    def __init__(self, matches: Optional[List[MatchRecord]] = None, parent=None):
        super().__init__(parent)
        self._all_records: List[MatchRecord] = matches or []
        self._filtered_records: List[MatchRecord] = list(self._all_records)

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return len(self._filtered_records)

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return len(COLUMNS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = int(Qt.ItemDataRole.DisplayRole)) -> Any:
        if orientation == Qt.Orientation.Horizontal and role == int(Qt.ItemDataRole.DisplayRole):
            return COLUMNS[section]
        return None

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = int(Qt.ItemDataRole.DisplayRole)) -> Any:
        if not index.isValid() or index.row() >= len(self._filtered_records):
            return None

        m = self._filtered_records[index.row()]
        col = index.column()

        ra = m.record_a
        rb = m.record_b

        if role == int(Qt.ItemDataRole.DisplayRole):
            if col == 0:
                return m.match_status.value
            elif col == 1:
                return (rb.supplier_gstin if rb else (ra.supplier_gstin if ra else ""))
            elif col == 2:
                return (rb.supplier_name if rb and rb.supplier_name else (ra.supplier_name if ra else ""))
            elif col == 3:
                return ra.raw_invoice_number if ra else "-"
            elif col == 4:
                return rb.raw_invoice_number if rb else "-"
            elif col == 5:
                rec_d = rb if (rb and rb.invoice_date) else ra
                return rec_d.invoice_date.isoformat() if (rec_d and rec_d.invoice_date) else "-"
            elif col == 6:
                return m.match_level.value
            elif col == 7:
                return f"{ra.taxable_value:,.2f}" if ra else "-"
            elif col == 8:
                return f"{rb.taxable_value:,.2f}" if rb else "-"
            elif col == 9:
                return f"{m.diff_taxable:+,.2f}"
            elif col == 10:
                return f"{ra.calculate_total_tax():,.2f}" if ra else "-"
            elif col == 11:
                return f"{rb.calculate_total_tax():,.2f}" if rb else "-"
            elif col == 12:
                return f"{m.diff_total_tax:+,.2f}"
            elif col == 13:
                return m.review_status.value
            elif col == 14:
                return m.explanation

        elif role == int(Qt.ItemDataRole.TextAlignmentRole):
            # Right-align numeric columns
            if col in (7, 8, 9, 10, 11, 12):
                return int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            elif col in (0, 1, 3, 4, 5, 6, 13):
                return int(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            else:
                return int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        elif role == int(Qt.ItemDataRole.ForegroundRole):
            # Color coding for status and differences
            if col == 0:
                if m.match_status == MatchStatus.MATCHED:
                    return QColor("#10b981")  # Emerald
                elif m.match_status == MatchStatus.MATCHED_WITH_DIFFERENCE:
                    return QColor("#f59e0b")  # Amber
                elif m.match_status == MatchStatus.MISSING_IN_SOURCE_A:
                    return QColor("#ef4444")  # Red
                elif m.match_status == MatchStatus.MISSING_IN_SOURCE_B:
                    return QColor("#8b5cf6")  # Purple
            elif col in (9, 12):
                diff_val = m.diff_taxable if col == 9 else m.diff_total_tax
                if diff_val != Decimal("0.00"):
                    return QColor("#f59e0b")

        return None

    def get_record(self, row: int) -> Optional[MatchRecord]:
        """Return match record at given filtered row index."""
        if 0 <= row < len(self._filtered_records):
            return self._filtered_records[row]
        return None

    def set_records(self, matches: List[MatchRecord]):
        """Replace records and reset table view."""
        self.beginResetModel()
        self._all_records = matches
        self._filtered_records = list(matches)
        self.endResetModel()

    def filter(self, status_filter: Optional[str] = None, search_query: str = ""):
        """Filter in-memory table instantaneously."""
        self.beginResetModel()
        filtered = self._all_records

        if status_filter and status_filter != "ALL":
            filtered = [m for m in filtered if m.match_status.value == status_filter]

        if search_query:
            q = search_query.strip().lower()
            res = []
            for m in filtered:
                ra = m.record_a
                rb = m.record_b
                gstin = (rb.supplier_gstin if (rb and rb.supplier_gstin) else (ra.supplier_gstin if (ra and ra.supplier_gstin) else "")).lower()
                name_str = (rb.supplier_name if (rb and rb.supplier_name) else (ra.supplier_name if (ra and ra.supplier_name) else "")) or ""
                name = name_str.lower()
                inv_a = (ra.raw_invoice_number if (ra and ra.raw_invoice_number) else "").lower()
                inv_b = (rb.raw_invoice_number if (rb and rb.raw_invoice_number) else "").lower()
                if q in gstin or q in name or q in inv_a or q in inv_b:
                    res.append(m)
            filtered = res

        self._filtered_records = filtered
        self.endResetModel()
