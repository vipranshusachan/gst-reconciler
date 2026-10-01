"""Synthetic GST Dataset Generator for Testing and Demo."""

from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
import random
import openpyxl

VENDORS = [
    ("27AABCT3518Q1Z6", "TATA CONSULTANCY SERVICES LIMITED", "27"),
    ("29AAACB2002M1ZR", "INFOSYS LIMITED", "29"),
    ("07AAACA1234P1Z1", "BHARTI AIRTEL LIMITED", "07"),
    ("24AAACL5678B1ZH", "LARSEN & TOUBRO LIMITED", "24"),
    ("06AAACR9988C1ZK", "RELIANCE RETAIL LIMITED", "06"),
    ("33AAACM4321D1ZN", "MRF TYRES LIMITED", "33"),
    ("19AAACI8765E1ZQ", "ITC LIMITED", "19"),
    ("36AAACW1122F1ZS", "WIPRO ENTERPRISES LIMITED", "36"),
]


def generate_demo_files(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    file_2b = output_dir / "gstr2b_sample.xlsx"
    file_pr = output_dir / "purchase_register_sample.xlsx"

    wb_2b = openpyxl.Workbook()
    ws_2b = wb_2b.active
    ws_2b.title = "B2B"

    wb_pr = openpyxl.Workbook()
    ws_pr = wb_pr.active
    ws_pr.title = "Purchase Register"

    headers_2b = [
        "GSTIN of Supplier",
        "Trade/Legal Name",
        "Invoice number",
        "Invoice Date",
        "Invoice Value",
        "Place of supply",
        "Taxable Value",
        "Integrated Tax",
        "Central Tax",
        "State/UT Tax",
        "Cess",
    ]
    ws_2b.append(headers_2b)

    headers_pr = [
        "Vendor GSTIN",
        "Party Name",
        "Bill No",
        "Bill Date",
        "Taxable Amount",
        "CGST Amount",
        "SGST Amount",
        "IGST Amount",
        "Cess Amount",
        "Gross Total",
        "POS State",
    ]
    ws_pr.append(headers_pr)

    base_date = date(2026, 9, 1)

    # 1. Perfect Matches (30 records)
    for i in range(1, 31):
        gstin, name, pos = VENDORS[i % len(VENDORS)]
        inv_no = f"INV/2026/{1000 + i}"
        inv_date = base_date + timedelta(days=(i % 25))
        taxable = Decimal(f"{10000 + (i * 250)}.00")
        cgst = (taxable * Decimal("0.09")).quantize(Decimal("0.01"))
        sgst = (taxable * Decimal("0.09")).quantize(Decimal("0.01"))
        total = taxable + cgst + sgst

        ws_2b.append([gstin, name, inv_no, inv_date.strftime("%d/%m/%Y"), float(total), pos, float(taxable), 0.0, float(cgst), float(sgst), 0.0])
        ws_pr.append([gstin, name, inv_no, inv_date.strftime("%Y-%m-%d"), float(taxable), float(cgst), float(sgst), 0.0, 0.0, float(total), pos])

    # 2. Minor Rounding Differences (₹1 - ₹2 within tolerance) (10 records)
    for i in range(31, 41):
        gstin, name, pos = VENDORS[i % len(VENDORS)]
        inv_no = f"INV-2026-{1000 + i}"
        inv_date = base_date + timedelta(days=(i % 25))
        taxable_2b = Decimal(f"{25000 + (i * 100)}.00")
        taxable_pr = taxable_2b + Decimal("1.50")  # ₹1.50 difference
        cgst_2b = (taxable_2b * Decimal("0.09")).quantize(Decimal("0.01"))
        sgst_2b = (taxable_2b * Decimal("0.09")).quantize(Decimal("0.01"))
        cgst_pr = cgst_2b + Decimal("0.50")
        sgst_pr = sgst_2b + Decimal("0.50")
        total_2b = taxable_2b + cgst_2b + sgst_2b
        total_pr = taxable_pr + cgst_pr + sgst_pr

        ws_2b.append([gstin, name, inv_no, inv_date.strftime("%d/%m/%Y"), float(total_2b), pos, float(taxable_2b), 0.0, float(cgst_2b), float(sgst_2b), 0.0])
        ws_pr.append([gstin, name, inv_no, inv_date.strftime("%d-%b-%Y"), float(taxable_pr), float(cgst_pr), float(sgst_pr), 0.0, 0.0, float(total_pr), pos])

    # 3. Significant Value Mismatches (Exceeding Tolerance) (8 records)
    for i in range(41, 49):
        gstin, name, pos = VENDORS[i % len(VENDORS)]
        inv_no = f"BILL/26/{2000 + i}"
        inv_date = base_date + timedelta(days=10)
        taxable_2b = Decimal("50000.00")
        taxable_pr = Decimal("52500.00")  # ₹2,500 mismatch
        cgst_2b = Decimal("4500.00")
        sgst_2b = Decimal("4500.00")
        cgst_pr = Decimal("4725.00")
        sgst_pr = Decimal("4725.00")

        ws_2b.append([gstin, name, inv_no, inv_date.strftime("%d/%m/%Y"), 59000.00, pos, float(taxable_2b), 0.0, float(cgst_2b), float(sgst_2b), 0.0])
        ws_pr.append([gstin, name, inv_no, inv_date.strftime("%d/%m/%Y"), float(taxable_pr), float(cgst_pr), float(sgst_pr), 0.0, 0.0, 61950.00, pos])

    # 4. Normalized Formatting Variations (Leading zero / slash differences) (10 records)
    for i in range(50, 60):
        gstin, name, pos = VENDORS[i % len(VENDORS)]
        inv_2b = f"INV/00{i}/26"
        inv_pr = f"INV-{i}-26"
        inv_date = base_date + timedelta(days=15)
        taxable = Decimal("15000.00")
        igst = Decimal("2700.00")

        ws_2b.append([gstin, name, inv_2b, inv_date.strftime("%d/%m/%Y"), 17700.00, pos, float(taxable), float(igst), 0.0, 0.0, 0.0])
        ws_pr.append([gstin, name, inv_pr, inv_date.strftime("%Y-%m-%d"), float(taxable), 0.0, 0.0, float(igst), 0.0, 17700.00, pos])

    # 5. Fuzzy Match Candidate (Typo in Invoice Number) (4 records)
    for i in range(60, 64):
        gstin, name, pos = VENDORS[i % len(VENDORS)]
        inv_2b = f"DOC-990{i}"
        inv_pr = f"DOC-99O{i}"  # '0' vs 'O'
        inv_date = base_date + timedelta(days=18)
        taxable = Decimal("30000.00")
        igst = Decimal("5400.00")

        ws_2b.append([gstin, name, inv_2b, inv_date.strftime("%d/%m/%Y"), 35400.00, pos, float(taxable), float(igst), 0.0, 0.0, 0.0])
        ws_pr.append([gstin, name, inv_pr, inv_date.strftime("%d/%m/%Y"), float(taxable), 0.0, 0.0, float(igst), 0.0, 35400.00, pos])

    # 6. Missing in GSTR-2B (ITC at Risk) (8 records)
    for i in range(70, 78):
        gstin, name, pos = VENDORS[i % len(VENDORS)]
        inv_pr = f"UNFILED-INV-{3000 + i}"
        inv_date = base_date + timedelta(days=22)
        taxable = Decimal("40000.00")
        cgst = Decimal("3600.00")
        sgst = Decimal("3600.00")
        ws_pr.append([gstin, name, inv_pr, inv_date.strftime("%d/%m/%Y"), float(taxable), float(cgst), float(sgst), 0.0, 0.0, 47200.00, pos])

    # 7. Missing in Purchase Register (Unclaimed ITC) (6 records)
    for i in range(80, 86):
        gstin, name, pos = VENDORS[i % len(VENDORS)]
        inv_2b = f"MISSED-INV-{4000 + i}"
        inv_date = base_date + timedelta(days=25)
        taxable = Decimal("18000.00")
        igst = Decimal("3240.00")
        ws_2b.append([gstin, name, inv_2b, inv_date.strftime("%d/%m/%Y"), 21240.00, pos, float(taxable), float(igst), 0.0, 0.0, 0.0])

    # 8. Duplicate in Purchase Register (2 repeat records)
    dup_gstin, dup_name, dup_pos = VENDORS[0]
    ws_pr.append([dup_gstin, dup_name, "INV/2026/1001", "2026-09-02", 10250.00, 922.50, 922.50, 0.0, 0.0, 12095.00, dup_pos])

    wb_2b.save(file_2b)
    wb_pr.save(file_pr)
    return file_2b, file_pr


if __name__ == "__main__":
    out = Path(__file__).parent / "data"
    f1, f2 = generate_demo_files(out)
    print(f"Generated demo datasets:\n  1: {f1}\n  2: {f2}")
