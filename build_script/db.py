import sqlite3
from pathlib import Path


def init_db(db_path: Path) -> sqlite3.Connection:
    db_path.unlink(True)
    conn = sqlite3.connect(db_path)
    conn.executescript(
        """
        CREATE TABLE langcodes (
        lang_code TEXT COLLATE NOCASE,
        lang_name TEXT COLLATE NOCASE,
        in_lang TEXT COLLATE NOCASE,
        alt TEXT,
        PRIMARY KEY(lang_code, lang_name, in_lang));

        PRAGMA journal_mode = WAL;
        """
    )
    return conn


def create_index(conn: sqlite3.Connection) -> None:
    conn.execute("CREATE INDEX lang_name_index ON langcodes (lang_name, in_lang)")


def insert_data(
    conn: sqlite3.Connection,
    lang_code: str,
    lang_name: str,
    in_lang: str,
    alt: str = "",
) -> None:
    lang_code = lang_code.replace("_", "-")
    in_lang = in_lang.replace("_", "-")
    conn.execute(
        """
        INSERT INTO langcodes
        (lang_code, lang_name, in_lang, alt) VALUES(?, ?, ?, ?)
        ON CONFLICT(lang_code, lang_name, in_lang) DO UPDATE SET
        lang_code=excluded.lang_code,
        lang_name=excluded.lang_name,
        in_lang=excluded.in_lang
        """,
        (lang_code, lang_name, in_lang, alt),
    )
    # SQLite NOCASE only converts ASCII letters
    # https://www.sqlite.org/datatype3.html#collation
    for (sqlite_lower_name,) in conn.execute("SELECT lower(?)", (lang_name,)):
        if sqlite_lower_name != lang_name.lower():
            insert_data(conn, lang_code, lang_name.lower(), in_lang, alt)
