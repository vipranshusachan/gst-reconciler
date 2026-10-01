"""Excel reader with multi-sheet support and intelligent header detection."""

from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple
import openpyxl

from app.core.exceptions import IngestionError
from app.ingestion.reader_base import BaseTabularReader

GST_HEADER_KEYWORDS = [
    "gstin", "invoice", "taxable", "igst", "cgst", "sgst", "bill", "voucher", "party", "supplier"
]

class ExcelReader(BaseTabularReader):
    """Parses .xlsx and .xls Excel files."""

    def get_sheets(self, file_path: Path) -> List[str]:
        try:
            wb = openpyxl.load_workbook(file_path, read_only=True, keep_links=False)
            sheet_names = wb.sheetnames
            wb.close()
            return sheet_names
        except Exception as e:
            raise IngestionError(f"Failed to inspect Excel sheets in {file_path.name}: {e}")

    def read_tabular(
        self, file_path: Path, sheet_name: Optional[str] = None
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        try:
            wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True, keep_links=False)
            if sheet_name and sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
            else:
                ws = wb.active
        except Exception as e:
            raise IngestionError(f"Unable to open workbook {file_path.name}: {e}")

        rows = list(ws.iter_rows(values_only=True))
        wb.close()

        if not rows:
            return [], []

        # Find the header row by scanning first 15 rows for GST keywords
        header_row_idx = 0
        best_match_count = 0

        for idx, row in enumerate(rows[:15]):
            text_cells = [str(c).lower() for c in row if c is not None]
            match_count = sum(
                1 for c in text_cells if any(kw in c for kw in GST_HEADER_KEYWORDS)
            )
            if match_count > best_match_count:
                best_match_count = match_count
                header_row_idx = idx

        raw_headers = rows[header_row_idx]
        headers: List[str] = []
        for i, h in enumerate(raw_headers):
            val = str(h).strip() if h is not None else ""
            if not val:
                val = f"Column_{i+1}"
            headers.append(val)

        # Parse data rows
        data_rows: List[Dict[str, Any]] = []
        for row in rows[header_row_idx + 1:]:
            if not any(c is not None and str(c).strip() != "" for c in row):
                continue  # Skip completely empty rows

            row_dict: Dict[str, Any] = {}
            for col_idx, h in enumerate(headers):
                if col_idx < len(row):
                    cell_val = row[col_idx]
                    row_dict[h] = cell_val
                else:
                    row_dict[h] = None

            # Skip common footer total rows (e.g. "Total", "Grand Total")
            first_val = str(next((v for v in row_dict.values() if v is not None), "")).strip().lower()
            if first_val in ("total", "grand total", "sub total"):
                continue

            data_rows.append(row_dict)

        return headers, data_rows
