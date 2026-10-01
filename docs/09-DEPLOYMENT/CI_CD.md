# Continuous Integration & Delivery Pipeline

## 1. Pipeline Stages

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on Windows runners:

```
[Trigger: Push or PR]
         │
         ▼
[Stage 1: Lint & Code Quality]
   ├── Ruff Check
   ├── Ruff Format Check
   └── Mypy Strict Typing Check
         │
         ▼
[Stage 2: Automated Pytest Suite]
   ├── Unit Tests
   ├── Ingestion Integration Tests
   ├── Reconciliation Engine Tests
   └── Export Tests
         │
         ▼ (Only on Tag / Release)
[Stage 3: Windows PyInstaller Build]
   └── Package GSTReconciler.exe standalone distribution
         │
         ▼
[Stage 4: Inno Setup Compilation]
   └── Compile GSTReconciler-Setup-vX.Y.Z.exe
         │
         ▼
[Stage 5: Publish Release Artifacts]
   └── Attach .exe and checksums to GitHub Release
```
