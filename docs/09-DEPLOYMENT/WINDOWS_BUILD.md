# Windows Executable Build Guide

## 1. PyInstaller Build Configuration

GST Reconciler is packaged as a standalone native Windows binary using PyInstaller.

### Build Script (`build_windows.py`):
```python
import PyInstaller.__main__
from pathlib import Path

ROOT = Path(__file__).parent

PyInstaller.__main__.run([
    str(ROOT / "app" / "ui" / "app.py"),
    "--name=GSTReconciler",
    "--windowed",                 # No console window
    "--onedir",                   # Faster startup than --onefile
    "--noconfirm",
    "--clean",
    f"--add-data={ROOT / 'app' / 'ui' / 'assets'};assets",
    f"--add-data={ROOT / 'demo'};demo",
    "--icon=assets/app_icon.ico",
])
```

---

## 2. Dynamic Library & Hook Considerations

1. **PySide6 Plugins**: Ensure `platforms/qwindows.dll`, `styles/`, and `imageformats/` are properly bundled.
2. **OpenPyXL & SQLite**: Ensure sqlite3 DLLs and default schemas are included.
