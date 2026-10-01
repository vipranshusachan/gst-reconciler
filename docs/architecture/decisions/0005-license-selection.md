# ADR 0005: Open Source License Selection (Apache-2.0)

## Status
Accepted

## Context
Choosing an open-source license for a business-critical desktop accounting application requires balancing:
1. Community collaboration and transparency (encouraging contributions from CA firms, ERP developers, and SMEs).
2. Explicit patent protection and liability disclaimers (essential when processing financial/tax data).
3. Permissiveness for integration (enabling enterprises to adopt it without copyleft fears).

Evaluated options:
* **MIT License**: Minimal and widely recognized, but lacks explicit patent rights and detailed liability limitation clauses.
* **GPL-3.0**: Strong copyleft; prevents proprietary extensions and causes licensing friction with PySide6 (LGPLv3) and various commercial ERP connectors.
* **Apache License 2.0**: Permissive, includes an explicit patent grant, comprehensive copyright and trademark protections, and robust warranty/liability disclaimers.

## Decision
We license GST Reconciler under the **Apache License, Version 2.0**.

## Consequences
- Protects contributors and maintainers with explicit disclaimer of warranty for tax/accounting computations.
- Provides patent grants to downstream users.
- Broadly compatible with corporate environments and the Python desktop ecosystem.
