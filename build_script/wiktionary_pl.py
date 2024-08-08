from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "pl"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from xml.etree import ElementTree

    from db import insert_data
    from mediawiki_api import mediawiki_api_request

    # https://pl.wiktionary.org/wiki/Wikisłownik:Kody_języków
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {"action": "parse", "page": "Wikisłownik:Kody_języków", "prop": "text"},
        ("parse", "text"),
    )
    root = ElementTree.fromstring(page_html)
    count = 0
    for table in root.iterfind(".//tbody"):
        for tr_tag in table.iterfind(".//tr"):
            lang_name = ""
            for index, td_tag in enumerate(tr_tag.iterfind("td")):
                td_text = "".join(td_tag.itertext()).strip()
                if index == 0:
                    lang_name = td_text
                elif index == 1:
                    insert_data(conn, td_text, lang_name, WIKTIONARY_LANG_CODE)
                    count += 1
    logger.info(f"Added {count} data from Polish Wiktionary")
