import sqlite3
from pathlib import Path


def init_db(db_path: Path) -> sqlite3.Connection:
    db_path.unlink(True)
    conn = sqlite3.connect(db_path)
    conn.executescript(
        """
        CREATE TABLE langcodes (
        lang_code TEXT COLLATE NOCASE,
        lang_name TEXT,
        code_of_name TEXT COLLATE NOCASE,
        alt TEXT,
        PRIMARY KEY(lang_code, lang_name, code_of_name, alt));

        PRAGMA journal_mode = WAL;
        """
    )
    return conn


def insert_data(
    conn: sqlite3.Connection,
    lang_code: str,
    lang_name: str,
    code_of_name: str,
    alt: str | None,
) -> None:
    lang_code = lang_code.replace("_", "-")
    code_of_name = code_of_name.replace("_", "-")
    conn.execute(
        """
        INSERT INTO langcodes
        (lang_code, lang_name, code_of_name, alt) VALUES(?, ?, ?, ?)
        ON CONFLICT(lang_code, lang_name, code_of_name, alt) DO UPDATE SET
        lang_code=excluded.lang_code,
        lang_name=excluded.lang_name,
        code_of_name=excluded.code_of_name,
        alt=excluded.alt
        """,
        (lang_code, lang_name, code_of_name, alt),
    )
