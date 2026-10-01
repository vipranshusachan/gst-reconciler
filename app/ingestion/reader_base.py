"""Base Tabular Reader Interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class BaseTabularReader(ABC):
    """Abstract reader for tabular financial files."""

    @abstractmethod
    def get_sheets(self, file_path: Path) -> List[str]:
        """Return list of sheet names in the workbook, or ['Default'] for flat files."""
        pass

    @abstractmethod
    def read_tabular(
        self, file_path: Path, sheet_name: Optional[str] = None
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        """Read tabular file and return (headers, rows_as_dicts)."""
        pass
