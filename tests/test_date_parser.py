"""Unit tests for multi-format date parser."""

from datetime import date

from app.normalization.date_parser import parse_date


def test_parse_standard_dates():
    expected = date(2026, 9, 15)
    assert parse_date("15/09/2026") == expected
    assert parse_date("15-09-2026") == expected
    assert parse_date("2026-09-15") == expected
    assert parse_date("15.09.2026") == expected
    assert parse_date("15-Sep-2026") == expected


def test_parse_excel_serial_date():
    # Excel serial day 45000 is approximately March 2023
    d = parse_date(45000)
    assert isinstance(d, date)
    assert d.year == 2023


def test_parse_invalid_or_empty_dates():
    assert parse_date(None) is None
    assert parse_date("") is None
    assert parse_date("N/A") is None
    assert parse_date("-") is None
