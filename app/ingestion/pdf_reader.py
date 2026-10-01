"""PDF digital text reader."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.core.exceptions import IngestionError
from app.ingestion.reader_base import BaseTabularReader

try:
    import pdfplumber

    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False


class PDFReader(BaseTabularReader):
    """Parses digital vector PDFs containing invoice tables."""

    def get_sheets(self, file_path: Path) -> List[str]:
        if not HAS_PDFPLUMBER:
            return ["Page 1"]
        try:
            with pdfplumber.open(file_path) as pdf:
                return [f"Page {i + 1}" for i in range(len(pdf.pages))]
        except Exception:
            return ["Default"]

    def read_tabular(
        self, file_path: Path, sheet_name: Optional[str] = None
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        if not HAS_PDFPLUMBER:
            raise IngestionError("PDF processing requires pdfplumber (pip install pdfplumber).")

        all_rows: List[List[Any]] = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for tbl in tables:
                        for row in tbl:
                            if row and any(c is not None for c in row):
                                all_rows.append(row)
        except Exception as e:
            raise IngestionError(f"Failed to extract tables from PDF {file_path.name}: {e}") from e

        if not all_rows:
            return [], []

        raw_headers = all_rows[0]
        headers = [str(h).strip() if h else f"Col_{i + 1}" for i, h in enumerate(raw_headers)]

        data_rows: List[Dict[str, Any]] = []
        for r in all_rows[1:]:
            row_dict = {}
            for i, h in enumerate(headers):
                val = r[i] if i < len(r) else None
                row_dict[h] = str(val).strip() if val is not None else ""
            data_rows.append(row_dict)

        return headers, data_rows
