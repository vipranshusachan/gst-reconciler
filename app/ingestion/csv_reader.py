"""CSV reader with auto-delimiter sniffing and encoding fallback."""

import csv
import io
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.core.exceptions import IngestionError
from app.ingestion.reader_base import BaseTabularReader

GST_HEADER_KEYWORDS = [
    "gstin", "invoice", "taxable", "igst", "cgst", "sgst", "bill", "voucher", "party", "supplier"
]

ENCODINGS = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]

class CSVReader(BaseTabularReader):
    """Parses delimited text files (.csv, .tsv, .txt)."""

    def get_sheets(self, file_path: Path) -> List[str]:
        return ["Default"]

    def read_tabular(
        self, file_path: Path, sheet_name: Optional[str] = None
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        raw_bytes = file_path.read_bytes()
        text_content: Optional[str] = None

        for enc in ENCODINGS:
            try:
                text_content = raw_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue

        if text_content is None:
            raise IngestionError(f"Could not decode {file_path.name} with standard encodings.")

        # Sniff delimiter from sample
        sample = text_content[:4096]
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
            delimiter = dialect.delimiter
        except csv.Error:
            # Fallback to comma or semicolon check
            if sample.count(";") > sample.count(","):
                delimiter = ";"
            elif sample.count("\t") > sample.count(","):
                delimiter = "\t"
            elif sample.count("|") > sample.count(","):
                delimiter = "|"
            else:
                delimiter = ","

        reader = csv.reader(io.StringIO(text_content), delimiter=delimiter)
        raw_rows = list(reader)

        if not raw_rows:
            return [], []

        # Find header row
        header_row_idx = 0
        best_match_count = 0
        for idx, row in enumerate(raw_rows[:15]):
            text_cells = [c.lower() for c in row if c]
            match_count = sum(
                1 for c in text_cells if any(kw in c for kw in GST_HEADER_KEYWORDS)
            )
            if match_count > best_match_count:
                best_match_count = match_count
                header_row_idx = idx

        raw_headers = raw_rows[header_row_idx]
        headers: List[str] = []
        for i, h in enumerate(raw_headers):
            val = h.strip()
            if not val:
                val = f"Column_{i+1}"
            headers.append(val)

        data_rows: List[Dict[str, Any]] = []
        for row in raw_rows[header_row_idx + 1:]:
            if not any(c.strip() for c in row if c):
                continue

            row_dict: Dict[str, Any] = {}
            for col_idx, h in enumerate(headers):
                if col_idx < len(row):
                    row_dict[h] = row[col_idx].strip()
                else:
                    row_dict[h] = None

            # Skip trailing totals
            first_val = str(next((v for v in row_dict.values() if v is not None), "")).strip().lower()
            if first_val in ("total", "grand total", "sub total"):
                continue

            data_rows.append(row_dict)

        return headers, data_rows
