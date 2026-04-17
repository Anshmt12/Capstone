"""SQLite database for case management."""
import sqlite3
import os
from app.config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_number TEXT UNIQUE NOT NULL,
    case_title TEXT NOT NULL,
    court TEXT NOT NULL,
    judge TEXT,
    filing_date TEXT,
    decision_date TEXT,
    status TEXT CHECK(status IN ('pending','won','lost','settled','appealed')),
    case_type TEXT,
    legal_area TEXT,
    articles_invoked TEXT,  -- comma-separated article numbers
    opposing_counsel TEXT,
    client_name TEXT,
    summary TEXT,
    outcome_summary TEXT,
    damages_claimed REAL,
    damages_awarded REAL,
    priority TEXT CHECK(priority IN ('low','medium','high','critical'))
);

CREATE TABLE IF NOT EXISTS case_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER REFERENCES cases(id),
    event_date TEXT,
    event_type TEXT,
    description TEXT
);
"""


def get_db_path() -> str:
    os.makedirs(os.path.dirname(settings.SQLITE_DB) or ".", exist_ok=True)
    return settings.SQLITE_DB


def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(get_db_path())
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def get_table_info() -> str:
    """Return schema info for the LLM."""
    conn = get_connection()
    cursor = conn.execute("SELECT sql FROM sqlite_master WHERE type='table'")
    schemas = [row[0] for row in cursor if row[0]]
    conn.close()
    return "\n\n".join(schemas)
