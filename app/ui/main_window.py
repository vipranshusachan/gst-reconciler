"""Main Desktop Window with Sidebar Navigation and Central View Router."""

from pathlib import Path

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app import __version__
from app.application.service import ReconciliationService
from app.core.config import AppConfig
from app.domain.enums import ReviewStatus
from app.domain.models import ReconciliationSummary
from app.normalization.column_mapper import ColumnMapper
from app.ui.views.dashboard_view import DashboardView
from app.ui.views.explorer_view import IssueExplorerView
from app.ui.views.reports_view import ReportsView
from app.ui.views.settings_view import SettingsView
from app.ui.views.wizard_view import WizardView


class MainWindow(QMainWindow):
    """Main Application Window with Sidebar and View Router."""

    def __init__(self, service: ReconciliationService, config: AppConfig):
        super().__init__()
        self.service = service
        self.config = config

        self.setWindowTitle(f"GST Reconciler v{__version__} — Indian Tax Reconciliation")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 650)

        # Central Container (Bright & Clean Enterprise Canvas)
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f8fafc; color: #0f172a;")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar
        sidebar = self._build_sidebar()
        root_layout.addWidget(sidebar)

        # Central Stacked Views
        self.stack = QStackedWidget()
        self.dashboard_view = DashboardView()
        self.wizard_view = WizardView(self.service)
        self.explorer_view = IssueExplorerView()
        self.reports_view = ReportsView(self.service)
        self.settings_view = SettingsView(self.config)

        self.stack.addWidget(self.dashboard_view)  # Index 0
        self.stack.addWidget(self.wizard_view)  # Index 1
        self.stack.addWidget(self.explorer_view)  # Index 2
        self.stack.addWidget(self.reports_view)  # Index 3
        self.stack.addWidget(self.settings_view)  # Index 4

        root_layout.addWidget(self.stack)

        # Signal Connections
        self.dashboard_view.navigate_to_wizard.connect(lambda: self._navigate_to(1))
        self.dashboard_view.load_demo_requested.connect(self._load_demo_data)
        self.wizard_view.reconciliation_completed.connect(self._on_reconciliation_done)
        self.wizard_view.cancel_requested.connect(lambda: self._navigate_to(0))
        self.explorer_view.review_updated.connect(self._on_review_updated)

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #0f172a;
                border-right: 1px solid #1e293b;
            }
            QPushButton {
                text-align: left;
                padding: 12px 18px;
                border: none;
                border-radius: 8px;
                color: #cbd5e1;
                font-size: 13px;
                font-weight: 600;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #1e293b;
                color: #ffffff;
            }
            QPushButton:checked {
                background-color: #2563eb;
                color: #ffffff;
                font-weight: 700;
            }
        """)

        lay = QVBoxLayout(sidebar)
        lay.setContentsMargins(18, 24, 18, 24)
        lay.setSpacing(8)

        # Brand Logo / Title
        brand_box = QVBoxLayout()
        lbl_app = QLabel("GST RECONCILER")
        lbl_app.setStyleSheet(
            "color: #60a5fa; font-size: 17px; font-weight: 800; letter-spacing: 1px;"
        )
        brand_box.addWidget(lbl_app)

        lbl_desc = QLabel("Intelligent Tax Matcher")
        lbl_desc.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 500;")
        brand_box.addWidget(lbl_desc)
        lay.addLayout(brand_box)

        lay.addSpacing(20)

        # Nav Buttons
        self.btn_dash = QPushButton("📊  Dashboard")
        self.btn_dash.setCheckable(True)
        self.btn_dash.setChecked(True)
        self.btn_dash.clicked.connect(lambda: self._navigate_to(0))
        lay.addWidget(self.btn_dash)

        self.btn_wiz = QPushButton("🚀  Reconcile Wizard")
        self.btn_wiz.setCheckable(True)
        self.btn_wiz.clicked.connect(lambda: self._navigate_to(1))
        lay.addWidget(self.btn_wiz)

        self.btn_exp = QPushButton("📋  Issue Explorer")
        self.btn_exp.setCheckable(True)
        self.btn_exp.clicked.connect(lambda: self._navigate_to(2))
        lay.addWidget(self.btn_exp)

        self.btn_rep = QPushButton("📈  Reports & Export")
        self.btn_rep.setCheckable(True)
        self.btn_rep.clicked.connect(lambda: self._navigate_to(3))
        lay.addWidget(self.btn_rep)

        self.btn_set = QPushButton("⚙️  Settings")
        self.btn_set.setCheckable(True)
        self.btn_set.clicked.connect(lambda: self._navigate_to(4))
        lay.addWidget(self.btn_set)

        lay.addStretch()

        # Version & Privacy Badge
        ver_box = QVBoxLayout()
        lbl_priv = QLabel("🛡️ 100% Offline & Private")
        lbl_priv.setStyleSheet("color: #10b981; font-size: 11px; font-weight: bold;")
        ver_box.addWidget(lbl_priv)

        lbl_ver = QLabel(f"Version {__version__}")
        lbl_ver.setStyleSheet("color: #64748b; font-size: 11px;")
        ver_box.addWidget(lbl_ver)
        lay.addLayout(ver_box)

        return sidebar

    def _navigate_to(self, index: int):
        self.stack.setCurrentIndex(index)
        buttons = [self.btn_dash, self.btn_wiz, self.btn_exp, self.btn_rep, self.btn_set]
        for idx, btn in enumerate(buttons):
            btn.setChecked(idx == index)

    def _on_reconciliation_done(self, summary: ReconciliationSummary):
        self.dashboard_view.update_summary(summary)
        self.explorer_view.load_summary(summary)
        self.reports_view.set_summary(summary)
        self._navigate_to(0)  # Jump back to dashboard

    def _on_review_updated(self, match_id: str, new_status: str, note: str):
        self.service.repo.update_match_review(match_id, ReviewStatus(new_status), note)

    def _load_demo_data(self):
        """One-click demo reconciliation execution."""
        demo_dir = Path(__file__).parent.parent.parent / "demo" / "data"
        file_a = demo_dir / "gstr2b_sample.xlsx"
        file_b = demo_dir / "purchase_register_sample.xlsx"

        if not file_a.exists() or not file_b.exists():
            from demo.generate_demo_data import generate_demo_files

            generate_demo_files(demo_dir)

        # Ingest and map
        _, h_a, _ = self.service.inspect_file(file_a)
        m_a, _ = ColumnMapper.detect_mappings(h_a)
        records_a = self.service.ingest_and_normalize(file_a, "source_a", m_a, sheet_name="B2B")

        _, h_b, _ = self.service.inspect_file(file_b)
        m_b, _ = ColumnMapper.detect_mappings(h_b)
        records_b = self.service.ingest_and_normalize(file_b, "source_b", m_b)

        summary = self.service.reconcile(
            records_a=records_a,
            records_b=records_b,
            project_name="Demo GST Reconciliation",
            file_a_name=file_a.name,
            file_b_name=file_b.name,
        )

        self._on_reconciliation_done(summary)
        QMessageBox.information(
            self,
            "Demo Loaded",
            f"Successfully processed {summary.total_processed} demo records!\n"
            f"• Matched: {summary.total_matched}\n"
            f"• Differences: {summary.total_matched_with_diff}\n"
            f"• ITC at Risk: {summary.total_missing_in_a} (₹{summary.itc_at_risk_amount:,.2f})\n"
            f"• Unclaimed ITC: {summary.total_missing_in_b} (₹{summary.unclaimed_itc_amount:,.2f})",
        )
