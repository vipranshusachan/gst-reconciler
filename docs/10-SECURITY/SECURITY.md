# Security Documentation

## 1. Local Security Policy

GST Reconciler is an open-source, local-first application designed to process proprietary and sensitive financial data without cloud dependencies.

### Key Security Policies:
1. **Zero Outbound Sockets**: Core business modules have no networking code.
2. **Safe Deserialization**: The application avoids pickle or unsafe YAML loaders, relying strictly on standard JSON and SQLite.
3. **No Dynamic Code Injection**: Macro execution in spreadsheets is disabled.
4. **Dependency Auditing**: Automated GitHub Dependabot and pip-audit monitoring for CVEs across third-party dependencies.
