# Troubleshooting Guide

## Common Issues & Solutions

### 1. "Could not identify columns automatically"
* **Cause**: The Excel file has multiple introductory banner rows, merged headers, or unusual column labels.
* **Solution**: In Step 2 of the Import Wizard, manually select the correct column from the dropdown for each field (e.g. Map "Party GST" to "Supplier GSTIN"). Click "Save Mapping Profile" so you never have to map it again for this vendor or client format.

### 2. "Invoice numbers are matching, but marked as 'Difference'"
* **Cause**: The taxable value or tax amounts differ between your purchase register and the vendor's portal filing by more than the configured tolerance.
* **Solution**: Open the record in the **Side-by-Side Comparison** screen to see the exact field delta. If the difference is an acceptable minor round-off, increase your tolerance in Settings or mark the status as **Accepted**.

### 3. "Dates are not recognized"
* **Cause**: Dates are formatted with non-standard text (e.g. `2026/15/09` where month and day are inverted) or saved as irregular text strings.
* **Solution**: Ensure your ERP exports dates in standard formats (`DD/MM/YYYY`, `YYYY-MM-DD`, or `DD-Mon-YYYY`).

### 4. "Application says OCR provider is not available"
* **Cause**: Tesseract OCR is not installed or not in system PATH when trying to process a scanned image voucher.
* **Solution**: If you are processing digital PDFs or Excel/CSV files, OCR is not needed. If you need image OCR, install Tesseract OCR for Windows and point to it in Settings.
