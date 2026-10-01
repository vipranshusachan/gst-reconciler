import subprocess
import sys
from pathlib import Path

def build():
    root = Path(__file__).parent.resolve()
    entry_point = root / "app" / "ui" / "app.py"

    args = [
        sys.executable,
        "-m",
        "PyInstaller",
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
    result = subprocess.run(args)
    if result.returncode != 0:
        print("\nPyInstaller build failed or PyInstaller is not installed.")
        print("Install PyInstaller with: pip install pyinstaller")
        sys.exit(result.returncode)
    print("\nPyInstaller build completed successfully. Output located in /dist/GSTReconciler/")


if __name__ == "__main__":
    build()
