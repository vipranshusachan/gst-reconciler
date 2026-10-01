# Contributing Guidelines for Developers

Please review [Root CONTRIBUTING.md](file:///CONTRIBUTING.md) for overarching contribution policies.

## 1. Branching Strategy
* `main`: Production-ready branch. All releases are tagged from `main`.
* `feat/<feature-name>`: Feature development branches.
* `fix/<bug-name>`: Bug fix branches.

## 2. Testing Requirement
Every new ingestion format, reconciliation rule, or bug fix must include dedicated pytest test cases under `tests/`. PRs that decrease overall branch coverage will be rejected by CI.
