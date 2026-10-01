"""Integration tests for Ingestion and Reporting modules."""

from pathlib import Path

from app.application.service import ReconciliationService
from app.normalization.column_mapper import ColumnMapper


def test_excel_ingestion_and_reporting(tmp_path: Path):
    demo_dir = Path("demo/data")
    file_a = demo_dir / "gstr2b_sample.xlsx"
    file_b = demo_dir / "purchase_register_sample.xlsx"

    assert file_a.exists()
    assert file_b.exists()

    service = ReconciliationService()

    # Test inspection
    sheets_a, headers_a, rows_a = service.inspect_file(file_a)
    assert len(sheets_a) >= 1
    assert "B2B" in sheets_a
    assert len(headers_a) >= 8

    # Test mapping & ingestion
    mapping_a, _ = ColumnMapper.detect_mappings(headers_a)
    records_a = service.ingest_and_normalize(file_a, "source_a", mapping_a, sheet_name="B2B")
    assert len(records_a) > 0

    sheets_b, headers_b, rows_b = service.inspect_file(file_b)
    mapping_b, _ = ColumnMapper.detect_mappings(headers_b)
    records_b = service.ingest_and_normalize(file_b, "source_b", mapping_b)
    assert len(records_b) > 0

    # Test reconciliation
    summary = service.reconcile(records_a, records_b)
    assert summary.total_processed == len(records_a) + len(records_b)
    assert summary.total_matched > 0

    # Test Excel Export
    out_xlsx = tmp_path / "test_report.xlsx"
    service.export_excel(summary, out_xlsx)
    assert out_xlsx.exists()
    assert out_xlsx.stat().st_size > 5000

    # Test CSV Export
    out_csv = tmp_path / "test_report.csv"
    service.export_csv(summary, out_csv)
    assert out_csv.exists()
    assert out_csv.stat().st_size > 1000
