# ADR 0003: Storage Engine & Migration Strategy

## Status
Accepted

## Context
GST Reconciler must store user projects, mapping profiles, tolerance settings, reconciliation match ledgers, manual review decisions, and audit history locally on the user's computer.

Requirements:
1. Zero administration: No external database server (PostgreSQL, MySQL) can be required.
2. ACID compliance: Incomplete reconciliations or unexpected system shutdowns must never corrupt data.
3. Fast querying: Structured filtering across matched, mismatched, duplicate, and missing records.
4. Schema evolution: Smooth database migrations across application versions without user data loss.

Evaluated options:
* **SQLite (with WAL mode enabled) + Alembic / Custom Lightweight Migration Manager**: Zero configuration, single-file storage, ACID transactions, universally supported across all Windows operating systems.
* **DuckDB**: Great for analytics, but schema migrations and transactional multi-table updates are less mature for relational application state compared to SQLite.
* **JSON / Parquet flat files**: Easy to inspect, but lacks relational integrity, indexing for fast GUI pagination, and atomic write guarantees during power loss.

## Decision
We select **SQLite 3 with Write-Ahead Logging (WAL)** managed via **SQLAlchemy Core/ORM** and an automated versioned migration manager (`PRAGMA user_version`).

## Consequences
* Crash-resilient local storage stored in the user's AppData directory (`%APPDATA%/GSTReconciler/data.db`).
* Fast indexed pagination for GUI table views.
* Safe automatic migration pipeline that automatically backs up `data.db.bak` before applying schema migrations.
