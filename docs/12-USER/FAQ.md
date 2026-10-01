# Frequently Asked Questions (FAQ)

### Q: Does GST Reconciler upload my client data or invoices to the internet?
**A: No.** GST Reconciler is strictly an **offline-first desktop application**. All processing, calculations, and data storage occur entirely on your local machine.

### Q: Why do my invoice numbers match in Excel VLOOKUP, but fail in some other tools?
**A: Inconsistent formatting.** Vendors often write `INV/042` while ERPs write `INV-42` or `INV 0042`. GST Reconciler automatically cleans delimiters, trims leading zeros, and normalizes formatting across both files so these variations match automatically.

### Q: What is "ITC at Risk"?
**A: Input Tax Credit (ITC) on invoices you booked in your accounts, but which your vendor hasn't filed in GSTR-1.** Under Section 16(2)(aa) of the CGST Act, you cannot legally claim this credit in GSTR-3B until the vendor files their return.

### Q: Can I reconcile sales registers against GSTR-1?
**A: Yes.** Although typically used for Purchase vs GSTR-2B, you can select GSTR-1 as Source A and your Sales Register as Source B.

### Q: What should I set the tax tolerance to?
**A: Usually ₹2.00 or ₹5.00.** Different accounting systems round fractions of rupees differently. A ₹2.00 tolerance accommodates common round-off variations without flagging false alarms.
