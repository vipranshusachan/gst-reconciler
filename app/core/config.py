"""Configuration and settings manager for GST Reconciler."""

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
import os
import json

def get_default_data_dir() -> Path:
    """Return default application data directory in APPDATA on Windows or ~/.gst_reconciler."""
    appdata = os.getenv("APPDATA")
    if appdata:
        data_dir = Path(appdata) / "GSTReconciler"
    else:
        data_dir = Path.home() / ".gst_reconciler"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

@dataclass
class Tolerances:
    """Configurable tolerance thresholds for GST reconciliation."""
    taxable: Decimal = Decimal("5.00")
    cgst: Decimal = Decimal("2.00")
    sgst: Decimal = Decimal("2.00")
    igst: Decimal = Decimal("2.00")
    cess: Decimal = Decimal("2.00")
    total_tax: Decimal = Decimal("2.00")
    total_value: Decimal = Decimal("5.00")
    date_days: int = 30
    enable_fuzzy: bool = True
    fuzzy_threshold: float = 0.85

    def to_dict(self) -> dict:
        return {
            "taxable": float(self.taxable),
            "cgst": float(self.cgst),
            "sgst": float(self.sgst),
            "igst": float(self.igst),
            "cess": float(self.cess),
            "total_tax": float(self.total_tax),
            "total_value": float(self.total_value),
            "date_days": self.date_days,
            "enable_fuzzy": self.enable_fuzzy,
            "fuzzy_threshold": self.fuzzy_threshold,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tolerances":
        return cls(
            taxable=Decimal(str(data.get("taxable", "5.00"))),
            cgst=Decimal(str(data.get("cgst", "2.00"))),
            sgst=Decimal(str(data.get("sgst", "2.00"))),
            igst=Decimal(str(data.get("igst", "2.00"))),
            cess=Decimal(str(data.get("cess", "2.00"))),
            total_tax=Decimal(str(data.get("total_tax", "2.00"))),
            total_value=Decimal(str(data.get("total_value", "5.00"))),
            date_days=int(data.get("date_days", 30)),
            enable_fuzzy=bool(data.get("enable_fuzzy", True)),
            fuzzy_threshold=float(data.get("fuzzy_threshold", 0.85)),
        )

@dataclass
class AppConfig:
    """Global application settings."""
    data_dir: Path = field(default_factory=get_default_data_dir)
    tolerances: Tolerances = field(default_factory=Tolerances)
    check_updates_on_startup: bool = False
    theme: str = "dark"
    tesseract_path: str = ""

    @property
    def db_path(self) -> Path:
        return self.data_dir / "data.db"

    @property
    def config_file(self) -> Path:
        return self.data_dir / "settings.json"

    def save(self) -> None:
        """Persist settings to local JSON file."""
        data = {
            "tolerances": self.tolerances.to_dict(),
            "check_updates_on_startup": self.check_updates_on_startup,
            "theme": self.theme,
            "tesseract_path": self.tesseract_path,
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls) -> "AppConfig":
        """Load settings from local JSON file or return defaults."""
        config = cls()
        if config.config_file.exists():
            try:
                with open(config.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "tolerances" in data:
                    config.tolerances = Tolerances.from_dict(data["tolerances"])
                config.check_updates_on_startup = bool(data.get("check_updates_on_startup", False))
                config.theme = data.get("theme", "dark")
                config.tesseract_path = data.get("tesseract_path", "")
            except Exception:
                pass  # Fall back to defaults on corrupt config
        return config
