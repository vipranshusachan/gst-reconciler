# Auto-Update Architecture & Safety

## 1. Safe, Opt-In Update Checking

To maintain strict data privacy and prevent unexpected disruptions during critical tax filing deadlines:
1. **Never Force Auto-Updates**: The application only checks for updates if the user manually clicks "Check for Updates" in Settings, or explicitly enables the "Check for updates on startup" preference.
2. **Read-Only GitHub API Query**: Checks `https://api.github.com/repos/vipranshusachan/gst-reconciler/releases/latest` for semantic version tag comparison.
3. **User Confirmation Prompt**: If a newer release exists, the user is presented with a dialog displaying the release notes and a button to download the installer.
4. **Pre-Update Database Backup**: Prior to executing an upgrade, the application copies `%APPDATA%\GSTReconciler\data.db` to `data.db.backup_vX.Y.Z` to guarantee data integrity across schema migrations.
