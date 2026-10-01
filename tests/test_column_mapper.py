"""Unit tests for smart column mapping engine."""

from app.domain.models import MappingProfile
from app.normalization.column_mapper import ColumnMapper

def test_detect_mappings_gstr2b():
    headers = [
        "GSTIN of Supplier",
        "Trade/Legal Name",
        "Invoice number",
        "Invoice Date",
        "Invoice Value",
        "Taxable Value",
        "Integrated Tax",
        "Central Tax",
        "State/UT Tax",
        "Cess",
    ]
    mappings, confidences = ColumnMapper.detect_mappings(headers)

    assert mappings["GSTIN of Supplier"] == "supplier_gstin"
    assert mappings["Invoice number"] == "invoice_number"
    assert mappings["Invoice Date"] == "invoice_date"
    assert mappings["Taxable Value"] == "taxable_value"
    assert mappings["Integrated Tax"] == "igst"
    assert mappings["Central Tax"] == "cgst"
    assert mappings["State/UT Tax"] == "sgst"


def test_detect_mappings_tally():
    headers = [
        "Party GSTIN",
        "Party Name",
        "Voucher No.",
        "Date",
        "Taxable Amt",
        "CGST Amt",
        "SGST Amt",
        "Gross Total",
    ]
    mappings, confidences = ColumnMapper.detect_mappings(headers)

    assert mappings["Party GSTIN"] == "supplier_gstin"
    assert mappings["Voucher No."] == "invoice_number"
    assert mappings["Date"] == "invoice_date"
    assert mappings["Taxable Amt"] == "taxable_value"


def test_apply_profile():
    headers = ["Vendor_Tax_ID", "Bill_Ref", "Base_Amt"]
    profile = MappingProfile(
        profile_name="Custom ERP",
        mappings={"Vendor_Tax_ID": "supplier_gstin", "Bill_Ref": "invoice_number"}
    )

    applied_mappings, confs = ColumnMapper.apply_profile(headers, profile)
    assert applied_mappings["Vendor_Tax_ID"] == "supplier_gstin"
    assert applied_mappings["Bill_Ref"] == "invoice_number"
