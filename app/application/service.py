"""Application Service Layer orchestrating ingestion, normalization, matching, and persistence."""

from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from app.core.config import AppConfig, Tolerances
from app.core.logging import get_logger
from app.database.db import DatabaseManager
from app.database.migrations import run_migrations
from app.database.repository import ReconciliationRepository
from app.domain.models import InvoiceRecord, MappingProfile, ReconciliationSummary
from app.ingestion import get_reader_for_file
from app.normalization.column_mapper import ColumnMapper
from app.normalization.date_parser import parse_date
from app.normalization.gstin import normalize_gstin, validate_gstin
from app.normalization.invoice_no import normalize_invoice_number
from app.reconciliation.engine import ReconciliationEngine
from app.reporting.csv_exporter import CSVExporter
from app.reporting.excel_exporter import ExcelExporter

logger = get_logger(__name__)


def _to_decimal(val: Any) -> Decimal:
    """Safe conversion of raw string/numeric cell to Decimal."""
    if val is None:
        return Decimal("0.00")
    s = str(val).strip().replace(",", "").replace("₹", "").replace("Rs.", "").replace("Rs", "")
    if not s or s.lower() in ("nan", "none", "null", "-"):
        return Decimal("0.00")
    # Handle negative formatted in parentheses e.g. (100.50)
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1].strip()
    try:
        return Decimal(s).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return Decimal("0.00")


class ReconciliationService:
    """High-level service API for executing end-to-end reconciliation."""

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig.load()
        # Initialize SQLite database and run schema migrations
        run_migrations(self.config.db_path)
        self.db_manager = DatabaseManager(self.config.db_path)
        self.repo = ReconciliationRepository(self.db_manager)
        self.latest_summary: Optional[ReconciliationSummary] = None

    def inspect_file(self, file_path: Path) -> Tuple[List[str], List[str], List[Dict[str, Any]]]:
        """Inspect file sheets, headers, and first 5 preview rows.
        
        Returns:
            (sheet_names, headers, sample_preview_rows)
        """
        reader = get_reader_for_file(file_path)
        sheets = reader.get_sheets(file_path)
        selected_sheet = sheets[0] if sheets else None
        headers, rows = reader.read_tabular(file_path, sheet_name=selected_sheet)
        return sheets, headers, rows[:5]

    def ingest_and_normalize(
        self,
        file_path: Path,
        source_id: str,
        column_mapping: Dict[str, str],
        sheet_name: Optional[str] = None,
    ) -> List[InvoiceRecord]:
        """Parse raw file, apply mapping, and normalize into canonical InvoiceRecord entities."""
        reader = get_reader_for_file(file_path)
        headers, rows = reader.read_tabular(file_path, sheet_name=sheet_name)

        invoice_records: List[InvoiceRecord] = []

        for row_idx, row in enumerate(rows, 1):
            mapped_data: Dict[str, Any] = {}
            for src_col, canonical_key in column_mapping.items():
                if src_col in row:
                    mapped_data[canonical_key] = row[src_col]

            raw_gstin = str(mapped_data.get("supplier_gstin") or "").strip()
            raw_inv = str(mapped_data.get("invoice_number") or "").strip()
            raw_date = str(mapped_data.get("invoice_date") or "").strip()

            # Skip empty placeholder rows without invoice number or GSTIN
            if not raw_gstin and not raw_inv:
                continue

            is_valid_gstin, clean_gstin, gstin_err = validate_gstin(raw_gstin)
            clean_inv = normalize_invoice_number(raw_inv)
            clean_date = parse_date(raw_date)

            taxable = _to_decimal(mapped_data.get("taxable_value"))
            igst = _to_decimal(mapped_data.get("igst"))
            cgst = _to_decimal(mapped_data.get("cgst"))
            sgst = _to_decimal(mapped_data.get("sgst"))
            cess = _to_decimal(mapped_data.get("cess"))
            tot_val = _to_decimal(mapped_data.get("total_invoice_value"))

            rec = InvoiceRecord(
                source_id=source_id,
                source_file=file_path.name,
                source_row=row_idx,
                supplier_gstin=clean_gstin,
                raw_supplier_gstin=raw_gstin,
                supplier_name=str(mapped_data.get("supplier_name") or "").strip() or None,
                invoice_number=clean_inv,
                raw_invoice_number=raw_inv,
                invoice_date=clean_date,
                raw_invoice_date=raw_date,
                invoice_type=str(mapped_data.get("invoice_type") or "B2B").strip().upper(),
                taxable_value=taxable,
                igst=igst,
                cgst=cgst,
                sgst=sgst,
                cess=cess,
                total_tax=igst + cgst + sgst + cess,
                total_invoice_value=tot_val,
                place_of_supply=str(mapped_data.get("place_of_supply") or "").strip() or None,
                is_valid_gstin=is_valid_gstin,
                raw_data=row,
            )
            invoice_records.append(rec)

        return invoice_records

    def reconcile(
        self,
        records_a: List[InvoiceRecord],
        records_b: List[InvoiceRecord],
        tolerances: Optional[Tolerances] = None,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        project_name: str = "GST Reconciliation",
        file_a_name: str = "",
        file_b_name: str = "",
    ) -> ReconciliationSummary:
        """Run the core multi-tier matching engine and commit results to database."""
        tol = tolerances or self.config.tolerances
        engine = ReconciliationEngine(tolerances=tol)

        summary = engine.reconcile(
            records_a=records_a,
            records_b=records_b,
            progress_callback=progress_callback,
            project_name=project_name,
            file_a_name=file_a_name,
            file_b_name=file_b_name,
        )

        # Commit run to SQLite
        try:
            self.repo.save_run(summary)
        except Exception as e:
            logger.warning(f"Unable to persist run to SQLite: {e}")

        self.latest_summary = summary
        return summary

    def export_excel(self, summary: ReconciliationSummary, output_path: Path) -> Path:
        """Generate formatted Excel report."""
        return ExcelExporter.export(summary, output_path)

    def export_csv(self, summary: ReconciliationSummary, output_path: Path) -> Path:
        """Generate CSV export."""
        return CSVExporter.export(summary, output_path)
