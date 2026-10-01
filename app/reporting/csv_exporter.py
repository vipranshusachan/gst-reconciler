"""High-speed CSV Exporter for Reconciled Records."""

import csv
from pathlib import Path
from app.core.exceptions import ExportError
from app.domain.models import ReconciliationSummary

class CSVExporter:
    """Exports reconciled matches into a single flat CSV file."""

    @classmethod
    def export(cls, summary: ReconciliationSummary, output_path: Path) -> Path:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                headers = [
                    "match_id",
                    "match_status",
                    "match_level",
                    "confidence_score",
                    "supplier_gstin",
                    "supplier_name",
                    "invoice_number_a",
                    "invoice_number_b",
                    "invoice_date",
                    "taxable_a",
                    "taxable_b",
                    "diff_taxable",
                    "tax_a",
                    "tax_b",
                    "diff_total_tax",
                    "review_status",
                    "explanation",
                ]
                writer.writerow(headers)

                for m in summary.matches:
                    ra = m.record_a
                    rb = m.record_b
                    gstin = rb.supplier_gstin if rb else (ra.supplier_gstin if ra else "")
                    name = rb.supplier_name if rb and rb.supplier_name else (ra.supplier_name if ra else "")
                    inv_a = ra.raw_invoice_number if ra else ""
                    inv_b = rb.raw_invoice_number if rb else ""
                    rec_for_date = rb if (rb and rb.invoice_date) else ra
                    inv_date = rec_for_date.invoice_date.isoformat() if (rec_for_date and rec_for_date.invoice_date) else ""

                    taxable_a = str(ra.taxable_value) if ra else "0.00"
                    taxable_b = str(rb.taxable_value) if rb else "0.00"
                    tax_a = str(ra.calculate_total_tax()) if ra else "0.00"
                    tax_b = str(rb.calculate_total_tax()) if rb else "0.00"

                    writer.writerow([
                        m.match_id,
                        m.match_status.value,
                        m.match_level.value,
                        f"{m.confidence_score:.2f}",
                        gstin,
                        name,
                        inv_a,
                        inv_b,
                        inv_date,
                        taxable_a,
                        taxable_b,
                        str(m.diff_taxable),
                        tax_a,
                        tax_b,
                        str(m.diff_total_tax),
                        m.review_status.value,
                        m.explanation,
                    ])

            return output_path
        except Exception as e:
            raise ExportError(f"Failed to generate CSV report: {e}")
