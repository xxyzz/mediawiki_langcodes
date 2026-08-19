from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "pt"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from db import insert_data

    LANGUAGES = (
        ("Língua Franca Nova", "lfn"),
        ("Galego-Português Medieval", "roa-gpm"),
    )
    for lang_name, lang_code in LANGUAGES:
        insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
    logger.info(f"Added {len(LANGUAGES)} data from Portuguese Wiktionary")
