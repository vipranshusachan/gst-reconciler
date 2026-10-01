"""Settings and Preferences View."""

from decimal import Decimal

from PySide6.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.core.config import AppConfig


class SettingsView(QWidget):
    """Configuration interface for tolerances, OCR, and application preferences."""

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self.config = config

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
                padding: 16px;
            }
            QLineEdit, QDoubleSpinBox, QSpinBox {
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
        layout.setSpacing(20)

        lbl_title = QLabel("Settings & Reconciliation Rules")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f8fafc;")
        layout.addWidget(lbl_title)

        # Tolerances Frame
        frame_tol = QFrame()
        grid = QGridLayout(frame_tol)
        grid.setSpacing(14)

        grid.addWidget(QLabel("<b>Default Taxable Value Tolerance (₹):</b>"), 0, 0)
        self.spin_taxable = QDoubleSpinBox()
        self.spin_taxable.setRange(0.0, 100.0)
        self.spin_taxable.setValue(float(config.tolerances.taxable))
        grid.addWidget(self.spin_taxable, 0, 1)

        grid.addWidget(QLabel("<b>Default Tax Component Tolerance (₹):</b>"), 1, 0)
        self.spin_tax = QDoubleSpinBox()
        self.spin_tax.setRange(0.0, 50.0)
        self.spin_tax.setValue(float(config.tolerances.total_tax))
        grid.addWidget(self.spin_tax, 1, 1)

        grid.addWidget(QLabel("<b>Default Date Window Tolerance (Days):</b>"), 2, 0)
        self.spin_date = QSpinBox()
        self.spin_date.setRange(0, 90)
        self.spin_date.setValue(config.tolerances.date_days)
        grid.addWidget(self.spin_date, 2, 1)

        self.chk_fuzzy = QCheckBox("Enable Gated Fuzzy Matching by Default")
        self.chk_fuzzy.setChecked(config.tolerances.enable_fuzzy)
        grid.addWidget(self.chk_fuzzy, 3, 0, 1, 2)

        layout.addWidget(frame_tol)

        # OCR & Paths Frame
        frame_paths = QFrame()
        lay_p = QVBoxLayout(frame_paths)
        lay_p.addWidget(QLabel("<b>OCR Configuration (Optional)</b>"))
        h_tess = QHBoxLayout()
        self.txt_tess = QLineEdit(config.tesseract_path)
        self.txt_tess.setPlaceholderText("Path to tesseract.exe (leave empty if on system PATH)...")
        h_tess.addWidget(self.txt_tess)
        btn_browse_tess = QPushButton("Browse...")
        btn_browse_tess.clicked.connect(self._browse_tesseract)
        h_tess.addWidget(btn_browse_tess)
        lay_p.addLayout(h_tess)
        layout.addWidget(frame_paths)

        # Actions
        btn_save = QPushButton("Save Settings 💾")
        btn_save.setStyleSheet("background-color: #3b82f6; color: white;")
        btn_save.clicked.connect(self._save_settings)
        layout.addWidget(btn_save)

        layout.addStretch()

    def _browse_tesseract(self):
        path_str, _ = QFileDialog.getOpenFileName(
            self, "Locate tesseract.exe", "", "Executables (*.exe);;All Files (*.*)"
        )
        if path_str:
            self.txt_tess.setText(path_str)

    def _save_settings(self):
        self.config.tolerances.taxable = Decimal(str(self.spin_taxable.value()))
        self.config.tolerances.total_tax = Decimal(str(self.spin_tax.value()))
        self.config.tolerances.cgst = Decimal(str(self.spin_tax.value()))
        self.config.tolerances.sgst = Decimal(str(self.spin_tax.value()))
        self.config.tolerances.igst = Decimal(str(self.spin_tax.value()))
        self.config.tolerances.date_days = self.spin_date.value()
        self.config.tolerances.enable_fuzzy = self.chk_fuzzy.isChecked()
        self.config.tesseract_path = self.txt_tess.text().strip()

        self.config.save()
        QMessageBox.information(self, "Settings Saved", "Your configuration has been updated.")
