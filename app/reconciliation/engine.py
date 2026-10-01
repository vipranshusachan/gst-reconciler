"""Core Multi-Tier GST Reconciliation Engine."""

from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from typing import Callable, Dict, List, Optional, Set, Tuple

from app.core.config import Tolerances
from app.domain.enums import DiscrepancyType, MatchLevel, MatchStatus
from app.domain.models import InvoiceRecord, MatchRecord, ReconciliationSummary
from app.reconciliation.classifier import DiscrepancyClassifier
from app.reconciliation.difference import calculate_differences
from app.reconciliation.matching_rules import MatchingRule


class ReconciliationEngine:
    """Independent, high-performance reconciliation engine."""

    def __init__(self, tolerances: Optional[Tolerances] = None):
        self.tolerances = tolerances or Tolerances()

    def reconcile(
        self,
        records_a: List[InvoiceRecord],
        records_b: List[InvoiceRecord],
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        project_name: str = "GST Reconciliation",
        file_a_name: str = "",
        file_b_name: str = "",
    ) -> ReconciliationSummary:
        """Run the multi-tier reconciliation pipeline across Source A and Source B records."""
        total_steps = len(records_a) + len(records_b)
        step_counter = 0

        def update_progress(msg: str) -> None:
            nonlocal step_counter
            if progress_callback:
                progress_callback(min(step_counter, total_steps), max(total_steps, 1), msg)

        update_progress("Starting reconciliation: deduplicating records...")

        # Pass 0: Deduplication check within each source
        duplicates_a, clean_a = self._detect_duplicates(records_a)
        duplicates_b, clean_b = self._detect_duplicates(records_b)

        matched_results: List[MatchRecord] = []
        matched_a_ids: Set[str] = set()
        matched_b_ids: Set[str] = set()

        # Build index maps for Source B
        exact_map_b: Dict[str, List[InvoiceRecord]] = defaultdict(list)
        strong_map_b: Dict[str, List[InvoiceRecord]] = defaultdict(list)
        normalized_map_b: Dict[str, List[InvoiceRecord]] = defaultdict(list)

        for rec_b in clean_b:
            exact_map_b[MatchingRule.exact_key(rec_b)].append(rec_b)
            strong_map_b[MatchingRule.strong_key(rec_b)].append(rec_b)
            normalized_map_b[MatchingRule.normalized_key(rec_b)].append(rec_b)

        update_progress("Executing Level 1: Exact Matching...")

        # ---------------------------------------------------------------------
        # Pass 1: Level 1 - Exact Match (GSTIN, Raw InvNo, Date)
        # ---------------------------------------------------------------------
        for rec_a in clean_a:
            step_counter += 1
            if step_counter % 500 == 0:
                update_progress("Level 1 Exact Matching...")

            k_exact = MatchingRule.exact_key(rec_a)
            candidates = exact_map_b.get(k_exact, [])
            for cand_b in candidates:
                if cand_b.record_id not in matched_b_ids:
                    match_rec = self._create_match(rec_a, cand_b, MatchLevel.EXACT, 1.0)
                    matched_results.append(match_rec)
                    matched_a_ids.add(rec_a.record_id)
                    matched_b_ids.add(cand_b.record_id)
                    break

        update_progress("Executing Level 2: Strong Normalized Matching...")

        # ---------------------------------------------------------------------
        # Pass 2: Level 2 - Strong Match (GSTIN, Cleaned Alphanumeric InvNo)
        # ---------------------------------------------------------------------
        for rec_a in clean_a:
            if rec_a.record_id in matched_a_ids:
                continue

            k_strong = MatchingRule.strong_key(rec_a)
            candidates = strong_map_b.get(k_strong, [])
            for cand_b in candidates:
                if cand_b.record_id not in matched_b_ids:
                    match_rec = self._create_match(rec_a, cand_b, MatchLevel.STRONG, 0.95)
                    matched_results.append(match_rec)
                    matched_a_ids.add(rec_a.record_id)
                    matched_b_ids.add(cand_b.record_id)
                    break

        update_progress("Executing Level 3: Normalized Variation Matching...")

        # ---------------------------------------------------------------------
        # Pass 3: Level 3 - Normalized Variation Match (GSTIN, Normalized InvNo + Date Window)
        # ---------------------------------------------------------------------
        for rec_a in clean_a:
            if rec_a.record_id in matched_a_ids:
                continue

            k_norm = MatchingRule.normalized_key(rec_a)
            candidates = normalized_map_b.get(k_norm, [])
            for cand_b in candidates:
                if cand_b.record_id not in matched_b_ids:
                    # Check date window
                    if rec_a.invoice_date and cand_b.invoice_date:
                        diff_days = abs((cand_b.invoice_date - rec_a.invoice_date).days)
                        if diff_days > self.tolerances.date_days:
                            continue

                    match_rec = self._create_match(rec_a, cand_b, MatchLevel.NORMALIZED, 0.90)
                    matched_results.append(match_rec)
                    matched_a_ids.add(rec_a.record_id)
                    matched_b_ids.add(cand_b.record_id)
                    break

        # ---------------------------------------------------------------------
        # Pass 4: Level 4 - Gated Fuzzy Match (if enabled)
        # ---------------------------------------------------------------------
        if self.tolerances.enable_fuzzy:
            update_progress("Executing Level 4: Gated Fuzzy Matching...")
            unmatched_a = [r for r in clean_a if r.record_id not in matched_a_ids]
            unmatched_b = [r for r in clean_b if r.record_id not in matched_b_ids]

            # Index unmatched B by GSTIN for fast candidate pruning
            b_by_gstin: Dict[str, List[InvoiceRecord]] = defaultdict(list)
            for r in unmatched_b:
                if r.supplier_gstin:
                    b_by_gstin[r.supplier_gstin].append(r)

            for rec_a in unmatched_a:
                candidates = b_by_gstin.get(rec_a.supplier_gstin, [])
                best_cand: Optional[InvoiceRecord] = None
                best_score: float = 0.0

                for cand_b in candidates:
                    if cand_b.record_id in matched_b_ids:
                        continue
                    score = MatchingRule.fuzzy_match_candidate(
                        rec_a, cand_b, threshold=self.tolerances.fuzzy_threshold
                    )
                    if score and score > best_score:
                        best_score = score
                        best_cand = cand_b

                if best_cand and best_score >= self.tolerances.fuzzy_threshold:
                    match_rec = self._create_match(rec_a, best_cand, MatchLevel.FUZZY, best_score)
                    matched_results.append(match_rec)
                    matched_a_ids.add(rec_a.record_id)
                    matched_b_ids.add(best_cand.record_id)

        update_progress("Finalizing discrepancies and unmatched records...")

        # ---------------------------------------------------------------------
        # Pass 5: Unmatched Records in Source A -> MISSING_IN_SOURCE_B
        # ---------------------------------------------------------------------
        for rec_a in clean_a:
            if rec_a.record_id not in matched_a_ids:
                tax_a = rec_a.calculate_total_tax()
                match_rec = MatchRecord(
                    match_status=MatchStatus.MISSING_IN_SOURCE_B,
                    match_level=MatchLevel.NONE,
                    confidence_score=1.0,
                    record_a=rec_a,
                    record_b=None,
                    diff_taxable=-rec_a.taxable_value,
                    diff_igst=-rec_a.igst,
                    diff_cgst=-rec_a.cgst,
                    diff_sgst=-rec_a.sgst,
                    diff_cess=-rec_a.cess,
                    diff_total_tax=-tax_a,
                    diff_total_value=-(rec_a.total_invoice_value or (rec_a.taxable_value + tax_a)),
                    discrepancy_types=[DiscrepancyType.MISSING_IN_PURCHASE_REGISTER],
                    explanation=(
                        f"Invoice '{rec_a.raw_invoice_number}' from supplier '{rec_a.supplier_name or rec_a.supplier_gstin}' "
                        f"exists in GSTR-2B but was NOT found in your Purchase Register (Unclaimed ITC)."
                    ),
                )
                matched_results.append(match_rec)

        # ---------------------------------------------------------------------
        # Pass 6: Unmatched Records in Source B -> MISSING_IN_SOURCE_A (ITC at Risk)
        # ---------------------------------------------------------------------
        for rec_b in clean_b:
            if rec_b.record_id not in matched_b_ids:
                tax_b = rec_b.calculate_total_tax()
                match_rec = MatchRecord(
                    match_status=MatchStatus.MISSING_IN_SOURCE_A,
                    match_level=MatchLevel.NONE,
                    confidence_score=1.0,
                    record_a=None,
                    record_b=rec_b,
                    diff_taxable=rec_b.taxable_value,
                    diff_igst=rec_b.igst,
                    diff_cgst=rec_b.cgst,
                    diff_sgst=rec_b.sgst,
                    diff_cess=rec_b.cess,
                    diff_total_tax=tax_b,
                    diff_total_value=rec_b.total_invoice_value or (rec_b.taxable_value + tax_b),
                    discrepancy_types=[DiscrepancyType.MISSING_IN_PORTAL_2B],
                    explanation=(
                        f"Invoice '{rec_b.raw_invoice_number}' from supplier '{rec_b.supplier_name or rec_b.supplier_gstin}' "
                        f"is booked in your Purchase Register but missing from GSTR-2B (ITC at Risk!)."
                    ),
                )
                matched_results.append(match_rec)

        # ---------------------------------------------------------------------
        # Pass 7: Add duplicate records
        # ---------------------------------------------------------------------
        for dup_a in duplicates_a:
            tax_a = dup_a.calculate_total_tax()
            matched_results.append(
                MatchRecord(
                    match_status=MatchStatus.DUPLICATE,
                    match_level=MatchLevel.NONE,
                    record_a=dup_a,
                    record_b=None,
                    diff_taxable=Decimal("0.00"),
                    diff_total_tax=Decimal("0.00"),
                    discrepancy_types=[DiscrepancyType.DUPLICATE_IN_SOURCE],
                    explanation=f"Duplicate invoice '{dup_a.raw_invoice_number}' repeated in Source A.",
                )
            )

        for dup_b in duplicates_b:
            tax_b = dup_b.calculate_total_tax()
            matched_results.append(
                MatchRecord(
                    match_status=MatchStatus.DUPLICATE,
                    match_level=MatchLevel.NONE,
                    record_a=None,
                    record_b=dup_b,
                    diff_taxable=Decimal("0.00"),
                    diff_total_tax=Decimal("0.00"),
                    discrepancy_types=[DiscrepancyType.DUPLICATE_IN_SOURCE],
                    explanation=f"Duplicate invoice '{dup_b.raw_invoice_number}' repeated in Purchase Register.",
                )
            )

        # Build final summary
        summary = self._build_summary(
            records_a=records_a,
            records_b=records_b,
            matches=matched_results,
            duplicates_a_count=len(duplicates_a),
            duplicates_b_count=len(duplicates_b),
            project_name=project_name,
            file_a_name=file_a_name,
            file_b_name=file_b_name,
        )

        update_progress("Reconciliation completed successfully.")
        return summary

    def _create_match(
        self, rec_a: InvoiceRecord, rec_b: InvoiceRecord, level: MatchLevel, confidence: float
    ) -> MatchRecord:
        """Calculate differences, classify, and construct MatchRecord."""
        (
            diff_taxable,
            diff_igst,
            diff_cgst,
            diff_sgst,
            diff_cess,
            diff_total_tax,
            diff_total_val,
            is_within_tol,
        ) = calculate_differences(rec_a, rec_b, self.tolerances)

        discrepancies, explanation = DiscrepancyClassifier.classify(
            rec_a=rec_a,
            rec_b=rec_b,
            diff_taxable=diff_taxable,
            diff_igst=diff_igst,
            diff_cgst=diff_cgst,
            diff_sgst=diff_sgst,
            diff_cess=diff_cess,
            diff_total_tax=diff_total_tax,
            diff_total_val=diff_total_val,
            tolerances=self.tolerances,
            match_level=level.value,
        )

        status = MatchStatus.MATCHED if is_within_tol else MatchStatus.MATCHED_WITH_DIFFERENCE

        return MatchRecord(
            match_status=status,
            match_level=level,
            confidence_score=confidence,
            record_a=rec_a,
            record_b=rec_b,
            diff_taxable=diff_taxable,
            diff_igst=diff_igst,
            diff_cgst=diff_cgst,
            diff_sgst=diff_sgst,
            diff_cess=diff_cess,
            diff_total_tax=diff_total_tax,
            diff_total_value=diff_total_val,
            discrepancy_types=discrepancies,
            explanation=explanation,
        )

    def _detect_duplicates(
        self, records: List[InvoiceRecord]
    ) -> Tuple[List[InvoiceRecord], List[InvoiceRecord]]:
        """Identify duplicate invoices within the same source dataset.

        Returns:
            (duplicates, unique_records)
        """
        seen: Set[str] = set()
        duplicates: List[InvoiceRecord] = []
        unique_records: List[InvoiceRecord] = []

        for rec in records:
            core = MatchingRule.strong_key(rec)
            if core in seen:
                duplicates.append(rec)
            else:
                seen.add(core)
                unique_records.append(rec)

        return duplicates, unique_records

    def _build_summary(
        self,
        records_a: List[InvoiceRecord],
        records_b: List[InvoiceRecord],
        matches: List[MatchRecord],
        duplicates_a_count: int,
        duplicates_b_count: int,
        project_name: str,
        file_a_name: str,
        file_b_name: str,
    ) -> ReconciliationSummary:
        """Compute aggregated metrics for dashboard and reporting."""
        matched_count = sum(1 for m in matches if m.match_status == MatchStatus.MATCHED)
        diff_count = sum(
            1 for m in matches if m.match_status == MatchStatus.MATCHED_WITH_DIFFERENCE
        )
        missing_a_count = sum(
            1 for m in matches if m.match_status == MatchStatus.MISSING_IN_SOURCE_A
        )
        missing_b_count = sum(
            1 for m in matches if m.match_status == MatchStatus.MISSING_IN_SOURCE_B
        )

        tot_taxable_a = sum((r.taxable_value for r in records_a), Decimal("0.00"))
        tot_taxable_b = sum((r.taxable_value for r in records_b), Decimal("0.00"))
        tot_tax_a = sum((r.calculate_total_tax() for r in records_a), Decimal("0.00"))
        tot_tax_b = sum((r.calculate_total_tax() for r in records_b), Decimal("0.00"))

        net_diff_taxable = sum(
            (
                m.diff_taxable
                for m in matches
                if m.match_status in (MatchStatus.MATCHED, MatchStatus.MATCHED_WITH_DIFFERENCE)
            ),
            Decimal("0.00"),
        )
        net_diff_tax = sum(
            (
                m.diff_total_tax
                for m in matches
                if m.match_status in (MatchStatus.MATCHED, MatchStatus.MATCHED_WITH_DIFFERENCE)
            ),
            Decimal("0.00"),
        )

        # ITC at Risk: Tax on records booked in books but missing in 2B
        itc_at_risk = sum(
            (
                m.diff_total_tax
                for m in matches
                if m.match_status == MatchStatus.MISSING_IN_SOURCE_A
            ),
            Decimal("0.00"),
        )
        # Unclaimed ITC: Tax on records in 2B but missing in books
        unclaimed_itc = sum(
            (
                -m.diff_total_tax
                for m in matches
                if m.match_status == MatchStatus.MISSING_IN_SOURCE_B
            ),
            Decimal("0.00"),
        )

        return ReconciliationSummary(
            project_name=project_name,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source_a_file=file_a_name,
            source_b_file=file_b_name,
            total_records_a=len(records_a),
            total_records_b=len(records_b),
            total_processed=len(records_a) + len(records_b),
            total_matched=matched_count,
            total_matched_with_diff=diff_count,
            total_missing_in_a=missing_a_count,
            total_missing_in_b=missing_b_count,
            total_duplicates_a=duplicates_a_count,
            total_duplicates_b=duplicates_b_count,
            total_taxable_a=tot_taxable_a,
            total_taxable_b=tot_taxable_b,
            total_tax_a=tot_tax_a,
            total_tax_b=tot_tax_b,
            net_diff_taxable=net_diff_taxable,
            net_diff_tax=net_diff_tax,
            itc_at_risk_amount=itc_at_risk,
            unclaimed_itc_amount=unclaimed_itc,
            matches=matches,
        )
