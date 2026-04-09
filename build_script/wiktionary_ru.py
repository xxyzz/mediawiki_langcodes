from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "ru"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from db import insert_data

    EXTRA_LANG_NAMES = (("orv", "Древнерусский"),)
    for lang_code, lang_name in EXTRA_LANG_NAMES:
        insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
