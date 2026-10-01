"""Multi-Step Import and Reconciliation Wizard View."""

from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.application.service import ReconciliationService
from app.core.config import Tolerances
from app.domain.models import InvoiceRecord, ReconciliationSummary
from app.normalization.column_mapper import CANONICAL_FIELDS, ColumnMapper


class ReconciliationWorker(QThread):
    """Background worker thread for running reconciliation without freezing UI."""

    progress_signal = Signal(int, int, str)
    finished_signal = Signal(object)
    failed_signal = Signal(str)

    def __init__(
        self,
        service: ReconciliationService,
        file_a: Path,
        file_b: Path,
        mapping_a: Dict[str, str],
        mapping_b: Dict[str, str],
        sheet_a: Optional[str],
        sheet_b: Optional[str],
        tolerances: Tolerances,
    ):
        super().__init__()
        self.service = service
        self.file_a = file_a
        self.file_b = file_b
        self.mapping_a = mapping_a
        self.mapping_b = mapping_b
        self.sheet_a = sheet_a
        self.sheet_b = sheet_b
        self.tolerances = tolerances

    def run(self):
        try:
            self.progress_signal.emit(10, 100, f"Ingesting Source A: {self.file_a.name}...")
            records_a = self.service.ingest_and_normalize(
                self.file_a, "source_a", self.mapping_a, sheet_name=self.sheet_a
            )

            self.progress_signal.emit(30, 100, f"Ingesting Source B: {self.file_b.name}...")
            records_b = self.service.ingest_and_normalize(
                self.file_b, "source_b", self.mapping_b, sheet_name=self.sheet_b
            )

            def engine_progress(curr, tot, msg):
                pct = 40 + int((curr / max(tot, 1)) * 50)
                self.progress_signal.emit(pct, 100, msg)

            summary = self.service.reconcile(
                records_a=records_a,
                records_b=records_b,
                tolerances=self.tolerances,
                progress_callback=engine_progress,
                project_name=f"Reconciliation {self.file_a.stem} vs {self.file_b.stem}",
                file_a_name=self.file_a.name,
                file_b_name=self.file_b.name,
            )

            self.progress_signal.emit(100, 100, "Done!")
            self.finished_signal.emit(summary)
        except Exception as e:
            self.failed_signal.emit(str(e))


class WizardView(QWidget):
    """4-step import, mapping, tolerance setup, and reconciliation wizard."""

    reconciliation_completed = Signal(object)
    cancel_requested = Signal()

    def __init__(self, service: ReconciliationService, parent=None):
        super().__init__(parent)
        self.service = service
        self.file_a_path: Optional[Path] = None
        self.file_b_path: Optional[Path] = None
        self.headers_a: List[str] = []
        self.headers_b: List[str] = []
        self.mapping_a: Dict[str, str] = {}
        self.mapping_b: Dict[str, str] = {}

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
            }
            QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 6px 10px;
                color: #f8fafc;
            }
            QPushButton {
                padding: 8px 18px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(16)

        # Wizard Title & Step Indicator
        self.lbl_step = QLabel("Step 1 of 4: Select Reconciliation Source Files")
        self.lbl_step.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
        layout.addWidget(self.lbl_step)

        # Stacked Pages
        self.pages = QStackedWidget()
        self.pages.addWidget(self._build_step1_page())
        self.pages.addWidget(self._build_step2_page())
        self.pages.addWidget(self._build_step3_page())
        self.pages.addWidget(self._build_step4_page())
        layout.addWidget(self.pages)

        # Bottom Wizard Navigation Bar
        nav_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet("background-color: #334155; color: #94a3b8;")
        self.btn_cancel.clicked.connect(self.cancel_requested.emit)
        nav_layout.addWidget(self.btn_cancel)

        nav_layout.addStretch()

        self.btn_prev = QPushButton("← Back")
        self.btn_prev.setStyleSheet("background-color: #334155; color: #f8fafc;")
        self.btn_prev.setEnabled(False)
        self.btn_prev.clicked.connect(self._go_prev)
        nav_layout.addWidget(self.btn_prev)

        self.btn_next = QPushButton("Next: Verify Columns →")
        self.btn_next.setStyleSheet("background-color: #3b82f6; color: white;")
        self.btn_next.clicked.connect(self._go_next)
        nav_layout.addWidget(self.btn_next)

        layout.addLayout(nav_layout)

    # -------------------------------------------------------------------------
    # STEP 1: Choose Files
    # -------------------------------------------------------------------------
    def _build_step1_page(self) -> QWidget:
        page = QWidget()
        p_layout = QVBoxLayout(page)
        p_layout.setSpacing(16)

        # Source A Box (Portal GSTR-2B)
        frame_a = QFrame()
        lay_a = QVBoxLayout(frame_a)
        lay_a.addWidget(QLabel("<b>Source A: GST Portal Return (GSTR-2B / GSTR-1)</b>"))
        h_a = QHBoxLayout()
        self.txt_path_a = QLineEdit()
        self.txt_path_a.setReadOnly(True)
        self.txt_path_a.setPlaceholderText("Select GSTR-2B Excel or CSV file...")
        h_a.addWidget(self.txt_path_a)
        btn_browse_a = QPushButton("Browse...")
        btn_browse_a.clicked.connect(lambda: self._browse_file("A"))
        h_a.addWidget(btn_browse_a)
        lay_a.addLayout(h_a)

        sheet_h_a = QHBoxLayout()
        sheet_h_a.addWidget(QLabel("Sheet Name:"))
        self.combo_sheet_a = QComboBox()
        sheet_h_a.addWidget(self.combo_sheet_a)
        sheet_h_a.addStretch()
        lay_a.addLayout(sheet_h_a)
        p_layout.addWidget(frame_a)

        # Source B Box (Purchase Register)
        frame_b = QFrame()
        lay_b = QVBoxLayout(frame_b)
        lay_b.addWidget(QLabel("<b>Source B: Internal Accounting Books (Purchase / Sales Register)</b>"))
        h_b = QHBoxLayout()
        self.txt_path_b = QLineEdit()
        self.txt_path_b.setReadOnly(True)
        self.txt_path_b.setPlaceholderText("Select Purchase Register Excel or CSV file...")
        h_b.addWidget(self.txt_path_b)
        btn_browse_b = QPushButton("Browse...")
        btn_browse_b.clicked.connect(lambda: self._browse_file("B"))
        h_b.addWidget(btn_browse_b)
        lay_b.addLayout(h_b)

        sheet_h_b = QHBoxLayout()
        sheet_h_b.addWidget(QLabel("Sheet Name:"))
        self.combo_sheet_b = QComboBox()
        sheet_h_b.addWidget(self.combo_sheet_b)
        sheet_h_b.addStretch()
        lay_b.addLayout(sheet_h_b)
        p_layout.addWidget(frame_b)

        p_layout.addStretch()
        return page

    def _browse_file(self, target: str):
        path_str, _ = QFileDialog.getOpenFileName(
            self, f"Select Source {target} File", "", "Spreadsheets & Docs (*.xlsx *.xls *.csv *.tsv *.pdf);;All Files (*.*)"
        )
        if not path_str:
            return

        p = Path(path_str)
        if target == "A":
            self.file_a_path = p
            self.txt_path_a.setText(str(p))
            sheets, headers, _ = self.service.inspect_file(p)
            self.combo_sheet_a.clear()
            self.combo_sheet_a.addItems(sheets)
            self.headers_a = headers
        else:
            self.file_b_path = p
            self.txt_path_b.setText(str(p))
            sheets, headers, _ = self.service.inspect_file(p)
            self.combo_sheet_b.clear()
            self.combo_sheet_b.addItems(sheets)
            self.headers_b = headers

    # -------------------------------------------------------------------------
    # STEP 2: Column Mapping
    # -------------------------------------------------------------------------
    def _build_step2_page(self) -> QWidget:
        page = QWidget()
        p_layout = QVBoxLayout(page)

        desc = QLabel("Confirm that each accounting attribute is mapped to the right column in your files.")
        desc.setStyleSheet("color: #94a3b8; font-size: 12px;")
        p_layout.addWidget(desc)

        self.table_map = QTableWidget(len(CANONICAL_FIELDS), 3)
        self.table_map.setHorizontalHeaderLabels(["Accounting Attribute", "Source A (Portal) Column", "Source B (Books) Column"])
        self.table_map.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_map.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table_map.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table_map.verticalHeader().setVisible(False)
        p_layout.addWidget(self.table_map)

        return page

    def _populate_mapping_step(self):
        self.table_map.setRowCount(len(CANONICAL_FIELDS))
        self.mapping_a, _ = ColumnMapper.detect_mappings(self.headers_a)
        self.mapping_b, _ = ColumnMapper.detect_mappings(self.headers_b)

        # Invert mapping for quick lookup: canonical -> source
        a_by_canon = {v: k for k, v in self.mapping_a.items()}
        b_by_canon = {v: k for k, v in self.mapping_b.items()}

        for row_idx, (canon_key, canon_label) in enumerate(CANONICAL_FIELDS.items()):
            # Col 0: Label
            item_lbl = QTableWidgetItem(canon_label)
            item_lbl.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table_map.setItem(row_idx, 0, item_lbl)

            # Col 1: Combo for Source A
            cb_a = QComboBox()
            cb_a.addItem("-- Not Mapped --", "")
            for h in self.headers_a:
                cb_a.addItem(h, h)
            if canon_key in a_by_canon:
                cb_a.setCurrentText(a_by_canon[canon_key])
            self.table_map.setCellWidget(row_idx, 1, cb_a)

            # Col 2: Combo for Source B
            cb_b = QComboBox()
            cb_b.addItem("-- Not Mapped --", "")
            for h in self.headers_b:
                cb_b.addItem(h, h)
            if canon_key in b_by_canon:
                cb_b.setCurrentText(b_by_canon[canon_key])
            self.table_map.setCellWidget(row_idx, 2, cb_b)

    # -------------------------------------------------------------------------
    # STEP 3: Tolerances & Rules
    # -------------------------------------------------------------------------
    def _build_step3_page(self) -> QWidget:
        page = QWidget()
        p_layout = QVBoxLayout(page)

        frame = QFrame()
        grid = QGridLayout(frame)
        grid.setSpacing(16)

        grid.addWidget(QLabel("<b>Taxable Value Tolerance (₹):</b>"), 0, 0)
        self.spin_taxable = QDoubleSpinBox()
        self.spin_taxable.setRange(0.0, 100.0)
        self.spin_taxable.setValue(5.0)
        grid.addWidget(self.spin_taxable, 0, 1)

        grid.addWidget(QLabel("<b>Tax Amount Tolerance (₹):</b>"), 1, 0)
        self.spin_tax = QDoubleSpinBox()
        self.spin_tax.setRange(0.0, 50.0)
        self.spin_tax.setValue(2.0)
        grid.addWidget(self.spin_tax, 1, 1)

        grid.addWidget(QLabel("<b>Invoice Date Tolerance (Days):</b>"), 2, 0)
        self.spin_date = QSpinBox()
        self.spin_date.setRange(0, 90)
        self.spin_date.setValue(30)
        grid.addWidget(self.spin_date, 2, 1)

        self.chk_fuzzy = QCheckBox("Enable Gated Fuzzy Matching (Levenshtein Token Ratio >= 85%)")
        self.chk_fuzzy.setChecked(True)
        grid.addWidget(self.chk_fuzzy, 3, 0, 1, 2)

        p_layout.addWidget(frame)
        p_layout.addStretch()
        return page

    # -------------------------------------------------------------------------
    # STEP 4: Execution Progress
    # -------------------------------------------------------------------------
    def _build_step4_page(self) -> QWidget:
        page = QWidget()
        p_layout = QVBoxLayout(page)
        p_layout.addStretch()

        self.lbl_progress = QLabel("Initializing reconciliation...")
        self.lbl_progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_progress.setStyleSheet("font-size: 14px; font-weight: bold; color: #38bdf8;")
        p_layout.addWidget(self.lbl_progress)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #334155;
                border-radius: 6px;
                text-align: center;
                height: 24px;
                background-color: #1e293b;
                color: #f8fafc;
            }
            QProgressBar::chunk {
                background-color: #3b82f6;
                border-radius: 6px;
            }
        """)
        p_layout.addWidget(self.progress_bar)

        p_layout.addStretch()
        return page

    # -------------------------------------------------------------------------
    # Navigation Logic
    # -------------------------------------------------------------------------
    def _go_next(self):
        curr = self.pages.currentIndex()
        if curr == 0:
            if not self.file_a_path or not self.file_b_path:
                self.lbl_step.setText("⚠️ Please select both Source A and Source B files to continue.")
                return
            self._populate_mapping_step()
            self.pages.setCurrentIndex(1)
            self.lbl_step.setText("Step 2 of 4: Confirm Column Mappings")
            self.btn_prev.setEnabled(True)
            self.btn_next.setText("Next: Tolerances →")
        elif curr == 1:
            # Read user overrides from mapping table
            self.mapping_a = {}
            self.mapping_b = {}
            for row in range(self.table_map.rowCount()):
                canon_key = list(CANONICAL_FIELDS.keys())[row]
                cb_a = self.table_map.cellWidget(row, 1)
                cb_b = self.table_map.cellWidget(row, 2)
                if isinstance(cb_a, QComboBox) and cb_a.currentData():
                    self.mapping_a[str(cb_a.currentData())] = canon_key
                if isinstance(cb_b, QComboBox) and cb_b.currentData():
                    self.mapping_b[str(cb_b.currentData())] = canon_key

            self.pages.setCurrentIndex(2)
            self.lbl_step.setText("Step 3 of 4: Configure Tolerances & Rules")
            self.btn_next.setText("Run Reconciliation 🚀")
        elif curr == 2:
            self.pages.setCurrentIndex(3)
            self.lbl_step.setText("Step 4 of 4: Processing Reconciliation...")
            self.btn_prev.setEnabled(False)
            self.btn_next.setEnabled(False)
            self._run_reconciliation()

    def _go_prev(self):
        curr = self.pages.currentIndex()
        if curr == 1:
            self.pages.setCurrentIndex(0)
            self.lbl_step.setText("Step 1 of 4: Select Reconciliation Source Files")
            self.btn_prev.setEnabled(False)
            self.btn_next.setText("Next: Verify Columns →")
        elif curr == 2:
            self.pages.setCurrentIndex(1)
            self.lbl_step.setText("Step 2 of 4: Confirm Column Mappings")
            self.btn_next.setText("Next: Tolerances →")

    def _run_reconciliation(self):
        if not self.file_a_path or not self.file_b_path:
            self._on_failed("Both source files must be selected.")
            return

        tol = Tolerances(
            taxable=Decimal(str(self.spin_taxable.value())),
            cgst=Decimal(str(self.spin_tax.value())),
            sgst=Decimal(str(self.spin_tax.value())),
            igst=Decimal(str(self.spin_tax.value())),
            cess=Decimal(str(self.spin_tax.value())),
            total_tax=Decimal(str(self.spin_tax.value())),
            date_days=self.spin_date.value(),
            enable_fuzzy=self.chk_fuzzy.isChecked(),
        )

        sheet_a = self.combo_sheet_a.currentText() or None
        sheet_b = self.combo_sheet_b.currentText() or None

        self.worker = ReconciliationWorker(
            service=self.service,
            file_a=self.file_a_path,
            file_b=self.file_b_path,
            mapping_a=self.mapping_a,
            mapping_b=self.mapping_b,
            sheet_a=sheet_a,
            sheet_b=sheet_b,
            tolerances=tol,
        )
        self.worker.progress_signal.connect(self._on_progress)
        self.worker.finished_signal.connect(self._on_finished)
        self.worker.failed_signal.connect(self._on_failed)
        self.worker.start()

    def _on_progress(self, current: int, total: int, msg: str):
        self.progress_bar.setValue(current)
        self.lbl_progress.setText(msg)

    def _on_finished(self, summary: ReconciliationSummary):
        self.reconciliation_completed.emit(summary)

    def _on_failed(self, error: str):
        self.lbl_progress.setText(f"❌ Error: {error}")
        self.btn_prev.setEnabled(True)
