# Quality Assurance Release Checklist

Before tagging and publishing any release of GST Reconciler:

- [ ] **Automated Tests**: All unit and integration test suites pass (`pytest tests/`).
- [ ] **Code Quality**: Zero errors reported by `ruff check .` and `ruff format --check .`.
- [ ] **Type Safety**: Critical domain packages pass strict static analysis (`mypy app/`).
- [ ] **Performance Verification**: Benchmark test executes 50,000 synthetic records in < 4.0 seconds.
- [ ] **Memory Verification**: Process memory remains below 350 MB during full reconciliation.
- [ ] **Windows Packaging**: PyInstaller builds `GSTReconciler.exe` without missing runtime DLLs.
- [ ] **Installer Generation**: Inno Setup creates `GSTReconciler-Setup-vX.Y.Z.exe` with valid desktop shortcuts and uninstaller.
- [ ] **Clean Machine Smoke Test**: Application installs and launches on a clean Windows machine without Python pre-installed.
- [ ] **Data Safety**: No telemetry or outbound network calls verified via packet inspection.
- [ ] **Release Notes**: `CHANGELOG.md` updated with all notable improvements and bug fixes.
