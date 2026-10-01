"""Repository for database operations on Projects, Runs, Matches, and Profiles."""

import json
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from app.database.db import DatabaseManager
from app.database.schema import (
    MappingProfileEntity,
    MatchRecordEntity,
    ReconciliationRunEntity,
)
from app.domain.enums import ReviewStatus
from app.domain.models import (
    InvoiceRecord,
    MappingProfile,
    ReconciliationSummary,
)


def _serialize_invoice(rec: Optional[InvoiceRecord]) -> Optional[str]:
    if not rec:
        return None
    d = {
        "record_id": rec.record_id,
        "source_id": rec.source_id,
        "source_file": rec.source_file,
        "source_row": rec.source_row,
        "supplier_gstin": rec.supplier_gstin,
        "raw_supplier_gstin": rec.raw_supplier_gstin,
        "supplier_name": rec.supplier_name,
        "buyer_gstin": rec.buyer_gstin,
        "invoice_number": rec.invoice_number,
        "raw_invoice_number": rec.raw_invoice_number,
        "invoice_date": rec.invoice_date.isoformat() if rec.invoice_date else None,
        "invoice_type": rec.invoice_type,
        "taxable_value": str(rec.taxable_value),
        "igst": str(rec.igst),
        "cgst": str(rec.cgst),
        "sgst": str(rec.sgst),
        "cess": str(rec.cess),
        "total_tax": str(rec.total_tax),
        "total_invoice_value": str(rec.total_invoice_value),
        "place_of_supply": rec.place_of_supply,
        "reverse_charge": rec.reverse_charge,
        "is_valid_gstin": rec.is_valid_gstin,
    }
    return json.dumps(d)


def _deserialize_invoice(raw_json: Optional[str]) -> Optional[InvoiceRecord]:
    if not raw_json:
        return None
    d = json.loads(raw_json)
    from datetime import date

    d_date = date.fromisoformat(d["invoice_date"]) if d.get("invoice_date") else None
    return InvoiceRecord(
        record_id=d["record_id"],
        source_id=d["source_id"],
        source_file=d["source_file"],
        source_row=d["source_row"],
        supplier_gstin=d["supplier_gstin"],
        raw_supplier_gstin=d["raw_supplier_gstin"],
        supplier_name=d["supplier_name"],
        buyer_gstin=d["buyer_gstin"],
        invoice_number=d["invoice_number"],
        raw_invoice_number=d["raw_invoice_number"],
        invoice_date=d_date,
        invoice_type=d["invoice_type"],
        taxable_value=Decimal(d["taxable_value"]),
        igst=Decimal(d["igst"]),
        cgst=Decimal(d["cgst"]),
        sgst=Decimal(d["sgst"]),
        cess=Decimal(d["cess"]),
        total_tax=Decimal(d["total_tax"]),
        total_invoice_value=Decimal(d["total_invoice_value"]),
        place_of_supply=d["place_of_supply"],
        reverse_charge=d["reverse_charge"],
        is_valid_gstin=d["is_valid_gstin"],
    )


class ReconciliationRepository:
    """Manages transactional persistence for reconciliation state."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def save_run(self, summary: ReconciliationSummary) -> str:
        """Persist a complete reconciliation run and all child match records."""
        with self.db.get_session() as session:
            run_entity = ReconciliationRunEntity(
                id=summary.run_id,
                project_id=None,
                source_a_file=summary.source_a_file,
                source_b_file=summary.source_b_file,
                summary_json=json.dumps(
                    {
                        "total_records_a": summary.total_records_a,
                        "total_records_b": summary.total_records_b,
                        "total_processed": summary.total_processed,
                        "total_matched": summary.total_matched,
                        "total_matched_with_diff": summary.total_matched_with_diff,
                        "total_missing_in_a": summary.total_missing_in_a,
                        "total_missing_in_b": summary.total_missing_in_b,
                        "total_duplicates_a": summary.total_duplicates_a,
                        "total_duplicates_b": summary.total_duplicates_b,
                        "itc_at_risk_amount": str(summary.itc_at_risk_amount),
                        "unclaimed_itc_amount": str(summary.unclaimed_itc_amount),
                        "net_diff_taxable": str(summary.net_diff_taxable),
                        "net_diff_tax": str(summary.net_diff_tax),
                    }
                ),
            )
            session.add(run_entity)

            for m in summary.matches:
                gstin = (
                    m.record_b.supplier_gstin
                    if m.record_b
                    else (m.record_a.supplier_gstin if m.record_a else "")
                )
                inv_no = (
                    m.record_b.raw_invoice_number
                    if m.record_b
                    else (m.record_a.raw_invoice_number if m.record_a else "")
                )

                match_entity = MatchRecordEntity(
                    id=m.match_id,
                    run_id=summary.run_id,
                    match_status=m.match_status.value,
                    match_level=m.match_level.value,
                    confidence_score=m.confidence_score,
                    supplier_gstin=gstin,
                    invoice_number=inv_no,
                    diff_taxable=float(m.diff_taxable),
                    diff_total_tax=float(m.diff_total_tax),
                    diff_total_value=float(m.diff_total_value),
                    record_a_json=_serialize_invoice(m.record_a),
                    record_b_json=_serialize_invoice(m.record_b),
                    discrepancy_types_json=json.dumps([d.value for d in m.discrepancy_types]),
                    explanation=m.explanation,
                    review_status=m.review_status.value,
                    review_note=m.review_note,
                )
                session.add(match_entity)

            session.commit()
            return summary.run_id

    def update_match_review(
        self, match_id: str, status: ReviewStatus, note: Optional[str] = None
    ) -> bool:
        """Update review status of a match record."""
        with self.db.get_session() as session:
            entity = session.query(MatchRecordEntity).filter_by(id=match_id).first()
            if not entity:
                return False
            entity.review_status = status.value
            entity.review_note = note or ""
            entity.reviewed_at = datetime.now()
            session.commit()
            return True

    def save_mapping_profile(self, profile: MappingProfile) -> None:
        """Save or update a reusable column mapping profile."""
        with self.db.get_session() as session:
            existing = (
                session.query(MappingProfileEntity)
                .filter_by(profile_name=profile.profile_name)
                .first()
            )
            if existing:
                existing.mappings_json = json.dumps(profile.mappings)
                existing.description = profile.description
            else:
                entity = MappingProfileEntity(
                    id=profile.profile_id,
                    profile_name=profile.profile_name,
                    description=profile.description,
                    mappings_json=json.dumps(profile.mappings),
                )
                session.add(entity)
            session.commit()

    def get_mapping_profiles(self) -> List[MappingProfile]:
        """Fetch all saved mapping profiles."""
        with self.db.get_session() as session:
            entities = session.query(MappingProfileEntity).all()
            profiles: List[MappingProfile] = []
            for e in entities:
                p_id = str(e.id)
                p_name = str(e.profile_name)
                p_desc = str(e.description or "")
                p_map = json.loads(str(e.mappings_json))
                profiles.append(
                    MappingProfile(
                        profile_id=p_id,
                        profile_name=p_name,
                        description=p_desc,
                        mappings=p_map,
                    )
                )
            return profiles
