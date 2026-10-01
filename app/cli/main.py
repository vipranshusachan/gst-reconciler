"""Command-Line Interface for GST Reconciler."""

from decimal import Decimal
from pathlib import Path
import sys
import click

from app import __version__
from app.application.service import ReconciliationService
from app.core.config import Tolerances
from app.normalization.column_mapper import ColumnMapper


@click.group()
@click.version_option(version=__version__, prog_name="gst-reconciler")
def cli():
    """GST Reconciler — Offline-First Desktop Reconciliation Engine."""
    pass


@cli.command()
def gui():
    """Launch the PySide6 Desktop User Interface."""
    from app.ui.app import run_app
    sys.exit(run_app())


@cli.command()
@click.option("--source-a", "-a", required=True, type=click.Path(exists=True, path_type=Path), help="Path to Source A (e.g. GSTR-2B Excel/CSV)")
@click.option("--source-b", "-b", required=True, type=click.Path(exists=True, path_type=Path), help="Path to Source B (e.g. Purchase Register Excel/CSV)")
@click.option("--taxable-tolerance", default=5.0, type=float, help="Allowable taxable value difference in Rupees (default 5.0)")
@click.option("--tax-tolerance", default=2.0, type=float, help="Allowable tax component difference in Rupees (default 2.0)")
@click.option("--date-tolerance", default=30, type=int, help="Allowable date difference in days (default 30)")
@click.option("--export", "-e", type=click.Path(path_type=Path), help="Optional path to output Excel report (.xlsx)")
def reconcile(
    source_a: Path,
    source_b: Path,
    taxable_tolerance: float,
    tax_tolerance: float,
    date_tolerance: int,
    export: Path | None,
):
    """Run headless reconciliation between two files."""
    click.echo(f"Initializing GST Reconciler v{__version__}...")
    service = ReconciliationService()

    # Inspect & Auto-map Source A
    click.echo(f"Analyzing Source A: {source_a.name}")
    _, headers_a, _ = service.inspect_file(source_a)
    mapping_a, _ = ColumnMapper.detect_mappings(headers_a)
    records_a = service.ingest_and_normalize(source_a, "source_a", mapping_a)
    click.echo(f"  Ingested {len(records_a)} records from Source A")

    # Inspect & Auto-map Source B
    click.echo(f"Analyzing Source B: {source_b.name}")
    _, headers_b, _ = service.inspect_file(source_b)
    mapping_b, _ = ColumnMapper.detect_mappings(headers_b)
    records_b = service.ingest_and_normalize(source_b, "source_b", mapping_b)
    click.echo(f"  Ingested {len(records_b)} records from Source B")

    # Reconcile
    tolerances = Tolerances(
        taxable=Decimal(str(taxable_tolerance)),
        cgst=Decimal(str(tax_tolerance)),
        sgst=Decimal(str(tax_tolerance)),
        igst=Decimal(str(tax_tolerance)),
        cess=Decimal(str(tax_tolerance)),
        total_tax=Decimal(str(tax_tolerance)),
        date_days=date_tolerance,
    )

    def on_progress(current, total, msg):
        pct = (current / total * 100) if total else 0
        click.echo(f"  [{pct:5.1f}%] {msg}")

    click.echo("\nExecuting Reconciliation Matching Engine...")
    summary = service.reconcile(
        records_a=records_a,
        records_b=records_b,
        tolerances=tolerances,
        progress_callback=on_progress,
        file_a_name=source_a.name,
        file_b_name=source_b.name,
    )

    # Print summary
    click.echo("\n" + "=" * 55)
    click.echo("RECONCILIATION SUMMARY")
    click.echo("=" * 55)
    click.echo(f"Total Processed:            {summary.total_processed}")
    click.echo(f"Matched (Within Tolerance): {summary.total_matched} ({summary.match_rate_percentage}%)")
    click.echo(f"Matched with Differences:   {summary.total_matched_with_diff}")
    click.echo(f"ITC at Risk (Missing in 2B):{summary.total_missing_in_a} (Amount: Rs. {summary.itc_at_risk_amount:,.2f})")
    click.echo(f"Unclaimed (Missing in Books):{summary.total_missing_in_b} (Amount: Rs. {summary.unclaimed_itc_amount:,.2f})")
    click.echo(f"Net Tax Difference:         Rs. {summary.net_diff_tax:,.2f}")
    click.echo("=" * 55)

    if export:
        click.echo(f"\nExporting report to {export}...")
        service.export_excel(summary, export)
        click.echo("Report successfully generated!")


if __name__ == "__main__":
    cli()
