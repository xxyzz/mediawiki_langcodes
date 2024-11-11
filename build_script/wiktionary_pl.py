from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "pl"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from db import insert_data
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://pl.wiktionary.org/wiki/Wikisłownik:Kody_języków
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "Wikisłownik:Kody_języków",
            "prop": "text",
            "disablelimitreport": "1",
        },
        ("parse", "text"),
    )
    root = etree.fromstring(page_html, etree.HTMLParser())
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
                    if lang_name.startswith("język "):
                        insert_data(
                            conn,
                            td_text,
                            lang_name.removeprefix("język "),
                            WIKTIONARY_LANG_CODE,
                        )
                    count += 1
    logger.info(f"Added {count} data from Polish Wiktionary")
