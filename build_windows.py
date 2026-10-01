"""Windows Standalone PyInstaller Executable Build Script."""

import sys
from pathlib import Path

def build():
    try:
        import PyInstaller.__main__
    except ImportError:
        print("PyInstaller is not installed. Install with: pip install pyinstaller")
        sys.exit(1)

    root = Path(__file__).parent.resolve()
    entry_point = root / "app" / "ui" / "app.py"

    args = [
        str(entry_point),
        "--name=GSTReconciler",
        "--noconfirm",
        "--clean",
        "--windowed",                 # Non-console GUI window
        "--onedir",                   # High performance directory mode
        f"--add-data={root / 'demo'};demo",
        "--collect-all=openpyxl",
        "--collect-all=rapidfuzz",
    ]

    print("Building GST Reconciler standalone Windows executable with PyInstaller...")
    print(f"Command arguments: {' '.join(args)}")
    PyInstaller.__main__.run(args)
    print("\nPyInstaller build completed successfully. Output located in /dist/GSTReconciler/")


if __name__ == "__main__":
    build()
