# Tax Difference Calculation & Tolerances

## 1. Accounting Precision via Decimal

Binary 64-bit floating-point arithmetic introduces IEEE 754 precision artifacts (e.g. `0.1 + 0.2 = 0.30000000000000004`). In taxation and accounting, such inaccuracies are unacceptable.

GST Reconciler converts all financial fields into Python's native `Decimal` objects and rounds all difference computations using `ROUND_HALF_UP` to two decimal places (`0.01`).

---

## 2. Configurable Tolerance Configuration

Tolerances are configurable in `Settings`:

```python
@dataclass
class Tolerances:
    taxable: Decimal = Decimal("5.00")  # Maximum allowable taxable discrepancy (₹)
    cgst: Decimal = Decimal("2.00")  # Maximum allowable CGST discrepancy (₹)
    sgst: Decimal = Decimal("2.00")  # Maximum allowable SGST discrepancy (₹)
    igst: Decimal = Decimal("2.00")  # Maximum allowable IGST discrepancy (₹)
    cess: Decimal = Decimal("2.00")  # Maximum allowable Cess discrepancy (₹)
    total_value: Decimal = Decimal("5.00")  # Maximum allowable invoice gross discrepancy (₹)
    date_days: int = 30  # Allowable invoice date difference in days
```

### Evaluation Logic:
For each matched candidate pair $(A, B)$:
$$\Delta_{taxable} = |B.taxable - A.taxable|$$
$$\Delta_{tax} = |(B.igst + B.cgst + B.sgst + B.cess) - (A.igst + A.cgst + A.sgst + A.cess)|$$

If $\Delta_{taxable} \le tolerance.taxable$ AND $\Delta_{tax} \le tolerance.tax$:
$\rightarrow$ `MATCHED` (Status: Within Allowed Tolerance).
Otherwise:
$\rightarrow$ `MATCHED_WITH_DIFFERENCE`.
