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
    conn.executescript(
        """
        CREATE INDEX lang_name_index ON langcodes (lang_name, in_lang);
        CREATE INDEX alt_index ON langcodes (alt);
        """
    )


def insert_data(
    conn: sqlite3.Connection,
    lang_code: str,
    lang_name: str,
    in_lang: str,
    alt: str = "",
    update_row: bool = False,
) -> None:
    lang_code = lang_code.replace("_", "-")
    in_lang = in_lang.replace("_", "-")
    if update_row:
        conn.execute(
            """
            INSERT INTO langcodes
            (lang_code, lang_name, in_lang, alt) VALUES(?, ?, ?, ?)
            ON CONFLICT(lang_code, lang_name, in_lang) DO UPDATE SET
            lang_code=excluded.lang_code,
            lang_name=excluded.lang_name,
            in_lang=excluded.in_lang,
            alt=excluded.alt
            """,
            (lang_code, lang_name, in_lang, alt),
        )
    else:
        conn.execute(
            """
            INSERT OR IGNORE INTO langcodes
            (lang_code, lang_name, in_lang, alt) VALUES(?, ?, ?, ?)
            """,
            (
                lang_code,
                lang_name,
                in_lang,
                alt if code_in_lang_exists(conn, lang_code, in_lang) else "",
            ),
        )
    # SQLite NOCASE only converts ASCII letters
    # https://www.sqlite.org/datatype3.html#collation
    for (sqlite_lower_name,) in conn.execute("SELECT lower(?)", (lang_name,)):
        if sqlite_lower_name != lang_name.lower():
            insert_data(
                conn, lang_code, lang_name.lower(), in_lang, alt + "_lower", update_row
            )


def code_in_lang_exists(conn: sqlite3.Connection, lang_code: str, in_lang: str) -> bool:
    for _ in conn.execute(
        "SELECT lang_code FROM langcodes WHERE lang_code = ? AND in_lang = ? LIMIT 1",
        (lang_code, in_lang),
    ):
        return True
    return False


def lang_name_exists(conn: sqlite3.Connection, lang_name: str) -> bool:
    for _ in conn.execute(
        "SELECT lang_name FROM langcodes WHERE lang_name = ? LIMIT 1", (lang_name,)
    ):
        return True
    return False
