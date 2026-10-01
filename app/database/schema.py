"""SQLAlchemy Schema Definitions for SQLite persistence."""

import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def _utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

class ProjectEntity(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=_utc_now)
    updated_at = Column(DateTime, default=_utc_now, onupdate=_utc_now)
    description = Column(Text, nullable=True)

    runs = relationship("ReconciliationRunEntity", back_populates="project", cascade="all, delete-orphan")


class MappingProfileEntity(Base):
    __tablename__ = "mapping_profiles"

    id = Column(String(36), primary_key=True)
    profile_name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    mappings_json = Column(Text, nullable=False)  # JSON dictionary of source -> canonical
    created_at = Column(DateTime, default=_utc_now)


class ReconciliationRunEntity(Base):
    __tablename__ = "reconciliation_runs"

    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime, default=_utc_now)
    source_a_file = Column(String(255), nullable=False)
    source_b_file = Column(String(255), nullable=False)
    summary_json = Column(Text, nullable=False)  # Serialized ReconciliationSummary

    project = relationship("ProjectEntity", back_populates="runs")
    matches = relationship("MatchRecordEntity", back_populates="run", cascade="all, delete-orphan")


class MatchRecordEntity(Base):
    __tablename__ = "match_records"

    id = Column(String(36), primary_key=True)
    run_id = Column(String(36), ForeignKey("reconciliation_runs.id"), nullable=False)
    match_status = Column(String(50), nullable=False, index=True)
    match_level = Column(String(50), nullable=False)
    confidence_score = Column(Float, default=1.0)

    # Identifiers for fast indexed querying
    supplier_gstin = Column(String(20), index=True, nullable=True)
    invoice_number = Column(String(100), index=True, nullable=True)

    # Financial differences
    diff_taxable = Column(Numeric(15, 2), default=0.0)
    diff_total_tax = Column(Numeric(15, 2), default=0.0)
    diff_total_value = Column(Numeric(15, 2), default=0.0)

    # Full serialized canonical payloads
    record_a_json = Column(Text, nullable=True)
    record_b_json = Column(Text, nullable=True)
    discrepancy_types_json = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)

    # Review status
    review_status = Column(String(20), default="OPEN", index=True)
    review_note = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    run = relationship("ReconciliationRunEntity", back_populates="matches")
