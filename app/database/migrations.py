"""Automated versioned migration manager for SQLite."""

import datetime
from pathlib import Path
import shutil
import sqlite3
from app.core.exceptions import DatabaseError
from app.core.logging import get_logger
from app.database.schema import Base

logger = get_logger(__name__)

CURRENT_SCHEMA_VERSION = 1

def run_migrations(db_path: Path) -> None:
    """Check database schema version, back up if upgrading, and apply schema."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not db_path.exists()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA user_version")
    version = cursor.fetchone()[0]

    if not is_new and version < CURRENT_SCHEMA_VERSION and version > 0:
        # Create safety backup before upgrading
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = db_path.parent / f"{db_path.stem}_backup_v{version}_{timestamp}.db"
        logger.info(f"Backing up database from v{version} to {backup_path.name}")
        shutil.copy2(db_path, backup_path)

    # Apply Base metadata to create tables
    from app.database.db import DatabaseManager
    manager = DatabaseManager(db_path)
    Base.metadata.create_all(bind=manager.engine)

    cursor.execute(f"PRAGMA user_version = {CURRENT_SCHEMA_VERSION}")
    conn.commit()
    conn.close()
    logger.info(f"Database migrated to schema version {CURRENT_SCHEMA_VERSION}")
