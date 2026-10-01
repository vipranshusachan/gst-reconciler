"""Multi-format date parsing and normalization for Indian accounting files."""

import re
from datetime import date, datetime, timedelta
from typing import Any, Optional

EXCEL_EPOCH = datetime(1899, 12, 30)

DATE_FORMATS = [
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y-%m-%d",
    "%d/%m/%y",
    "%d-%m-%y",
    "%d.%m.%Y",
    "%d.%m.%y",
    "%d-%b-%Y",
    "%d-%B-%Y",
    "%d %b %Y",
    "%d %B %Y",
    "%Y/%m/%d",
    "%m/%d/%Y",
]


def parse_date(value: Any) -> Optional[date]:
    """Convert various date representations into a standard datetime.date."""
    if value is None:
        return None

    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    # Check for Excel numeric serial date (e.g. 45280)
    if isinstance(value, (int, float)):
        try:
            val_int = int(value)
            if 30000 <= val_int <= 60000:
                dt = EXCEL_EPOCH + timedelta(days=val_int)
                return dt.date()
        except (ValueError, OverflowError):
            pass

    text = str(value).strip()
    if not text or text.lower() in ("nan", "none", "null", "nat", "-"):
        return None

    # Strip timestamps if attached (e.g. "2026-09-15 00:00:00")
    text = re.sub(r"\s+[0-9]{1,2}:[0-9]{2}(?::[0-9]{2})?.*$", "", text)

    # Try each standard pattern
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    # Try regex fallback for e.g. 15-09-2026
    m = re.match(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})$", text)
    if m:
        d_str, m_str, y_str = m.groups()
        y = int(y_str)
        if y < 100:
            y += 2000
        try:
            return date(y, int(m_str), int(d_str))
        except ValueError:
            pass

    return None
