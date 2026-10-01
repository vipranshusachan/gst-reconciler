# User Personas

## Persona 1: Rajesh Sharma — Chartered Accountant (CA)
* **Role**: Senior Partner at a mid-sized tax advisory firm in Mumbai.
* **Context**: Handles monthly GSTR-3B filings for 40+ corporate and MSME clients. Each client exports their purchase register in a different format (Tally, Busy, SAP, custom Excel).
* **Pain Points**:
  - Spends hours manually executing `VLOOKUP` or `XLOOKUP` in Excel.
  - Minor invoice number differences (e.g. `INV/2026/042` vs `INV-2026-42`) cause lookups to fail, resulting in false negatives.
  - Client data confidentiality is paramount; cannot upload client financials to unvetted cloud software.
* **Goals**:
  - Fast, reliable reconciliation under 5 minutes per client.
  - Highlighting ITC at risk that can't be claimed in this month's GSTR-3B.
  - Automated report generation to email back to clients indicating vendor non-compliance.

## Persona 2: Priya Patel — In-House Enterprise Accountant
* **Role**: Accounts Payable & Indirect Taxation Specialist at a manufacturing company in Ahmedabad.
* **Context**: Processes 15,000 to 50,000 procurement invoices per month from hundreds of suppliers across multiple states.
* **Pain Points**:
  - Frequent minor tax differences (₹1 to ₹3) due to decimal rounding in different ERPs hold up payment clearances.
  - Duplicate invoices submitted by vendors across multiple purchase orders.
  - Excel slows down and crashes when processing large 50k+ row datasets.
* **Goals**:
  - High-performance, crash-free reconciliation of large datasets.
  - Configurable tolerance settings so ₹2 rounding differences are automatically cleared.
  - Instant duplicate detection before releasing vendor payments.

## Persona 3: Vikram Mehta — Small Business Owner / Trader
* **Role**: Managing Director of an electrical goods wholesale business in New Delhi.
* **Context**: Does not have an advanced accounting background. Relies on an accountant who visits once a week.
* **Pain Points**:
  - Intimidated by complex accounting jargon and complex ERP menus.
  - Frequently loses Input Tax Credit because suppliers forget to file GSTR-1 on time.
* **Goals**:
  - Straightforward drag-and-drop user experience.
  - Clear dashboard showing total money at risk ("Vendors who haven't uploaded invoices").
  - Simple 1-click export.
