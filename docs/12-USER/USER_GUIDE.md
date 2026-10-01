# User Guide — GST Reconciler

## Welcome to GST Reconciler

GST Reconciler is an intuitive Windows desktop application designed to eliminate the headache of comparing Goods and Services Tax records. It compares your **Purchase Register** (your accounting records) with **GSTR-2B** (vendor uploads on the GST Portal) and highlights exactly which invoices are matched, which have tax calculation differences, and which vendors haven't uploaded their invoices.

---

## ⚡ 1-Minute Installation (Easy for Everyone)

### 1. Download & Install
1. Head to [GitHub Releases](https://github.com/vipranshusachan/gst-reconciler/releases).
2. Download `GSTReconciler-Setup-v1.0.0.exe` (or the portable zip version).
3. Run the installer and click **Next** until complete.
4. Launch **GST Reconciler** from your Desktop or Start Menu.

> **Note for Windows SmartScreen**: If Windows displays "Windows protected your PC", simply click **"More info"** and then **"Run anyway"**. The application is 100% open-source, runs completely offline, and contains zero adware or trackers.

### 2. Instant Test with Demo Data
Want to test the app without preparing your own files?
1. Open GST Reconciler.
2. In the top bar or Dashboard, click **"Load Demo Sample"**.
3. Watch the app instantly populate the Dashboard, reconcile sample GSTR-2B and Purchase Register data, and explore real discrepancy examples!

---

## Key Features Walkthrough

### 1. The Executive Dashboard
Upon launching the application or completing a reconciliation, the Dashboard provides an immediate overview of your tax position:
* **Matched Percentage**: Proportion of invoices successfully matched.
* **Input Tax Credit at Risk**: Total tax amount for invoices booked in your accounts that your suppliers have not yet uploaded to GSTR-2B.
* **Unclaimed Input Tax Credit**: Invoices that appear in GSTR-2B but have not yet been recorded in your accounting books.
* **Tax Differences**: The total value of round-off or tax rate discrepancies.

### 2. The Import Wizard
1. Click **New Reconciliation** on the sidebar.
2. Select your **Source A** (typically your GSTR-2B Excel or CSV download from the GST Portal) and **Source B** (your Purchase Register exported from Tally, Busy, SAP, or Zoho).
3. The software will automatically inspect the columns and match them (e.g., "Supplier GSTIN" -> "GSTIN"). If any column is unmapped, select the correct column from the dropdown.
4. Review the tolerance settings (default: ₹5.00 for taxable amount, ₹2.00 for tax components).
5. Click **Run Reconciliation**.

### 3. The Issue Explorer
The Issue Explorer lists all records that require attention:
* Use the filter buttons at the top to focus on specific categories (e.g., **Missing in 2B**, **Tax Differences**, or **Duplicates**).
* Type in the search box to search for any vendor name, invoice number, or GSTIN.
* Double-click any row to open the **Side-by-Side Comparison** window.

### 4. Side-by-Side Comparison
This window shows your accounting record on the left and the GST portal record on the right. Any numbers that do not match are highlighted with warning badges. You can choose to mark the issue as:
* **Accepted**: You approve the difference (e.g., acceptable round-off).
* **Rejected**: The vendor made an error; issue requires debit note.
* **Ignored**: Do not include in follow-up.

### 5. Exporting Reports
Click **Export to Excel** to generate a stylized, multi-sheet workbook complete with executive summaries, matched sheets, and itemized discrepancy lists ready to be sent to vendors for correction.
