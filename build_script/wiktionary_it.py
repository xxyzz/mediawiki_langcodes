from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "it"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from db import insert_data
    from mediawiki_api import mediawiki_api_request

    # https://it.wiktionary.org/wiki/Wikizionario:switch_lang
    page_text = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "Wikizionario:switch_lang",
            "prop": "wikitext",
            "disablelimitreport": "1",
        },
        ("parse", "wikitext"),
    )
    count = 0
    for line in page_text.splitlines():
        if line.startswith("|") and "=" in line:
            line = line.strip("| \n")
            code, name = line.split("=")
            code = code.strip()
            name = name.strip()
            insert_data(conn, code, name, WIKTIONARY_LANG_CODE)
            count += 1

    logger.info(f"Added {count} data from Italian Wiktionary")
