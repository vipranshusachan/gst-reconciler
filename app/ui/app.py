"""Desktop Application Entry Point."""

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from app.application.service import ReconciliationService
from app.core.config import AppConfig
from app.ui.main_window import MainWindow


def run_app() -> int:
    """Initialize and run the PySide6 Desktop GUI."""
    # Enable high-DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("GST Reconciler")
    app.setOrganizationName("Open Source GST Community")

    # Set default modern UI font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Initialize domain service and config
    config = AppConfig.load()
    service = ReconciliationService(config)

    window = MainWindow(service, config)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(run_app())
