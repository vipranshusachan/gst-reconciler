"""Ingestion package for heterogeneous tabular files."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.core.exceptions import UnsupportedFileFormatError
from app.ingestion.csv_reader import CSVReader
from app.ingestion.excel_reader import ExcelReader
from app.ingestion.pdf_reader import PDFReader
from app.ingestion.reader_base import BaseTabularReader

def get_reader_for_file(file_path: Path) -> BaseTabularReader:
    """Factory to return appropriate reader for a given file extension."""
    suffix = file_path.suffix.lower()
    if suffix in (".xlsx", ".xls", ".xlsm"):
        return ExcelReader()
    elif suffix in (".csv", ".tsv", ".txt"):
        return CSVReader()
    elif suffix == ".pdf":
        return PDFReader()
    else:
        raise UnsupportedFileFormatError(
            f"Unsupported file format '{suffix}'. Supported: .xlsx, .xls, .csv, .tsv, .pdf",
            user_friendly_message=f"The format '{suffix}' is not supported. Please provide an Excel (.xlsx), CSV, or PDF file."
        )

__all__ = [
    "BaseTabularReader",
    "ExcelReader",
    "CSVReader",
    "PDFReader",
    "get_reader_for_file",
]
