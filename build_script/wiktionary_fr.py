from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "fr"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from db import insert_data
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_des_langues
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "Wiktionnaire:Liste_des_langues",
            "prop": "text",
            "disablelimitreport": "1",
        },
        ("parse", "text"),
    )
    root = etree.fromstring(page_html, etree.HTMLParser())
    count = 0
    for tr_tag in root.iterfind(".//tbody/tr"):
        lang_code = ""
        for index, td_tag in enumerate(tr_tag.iterfind("td")):
            td_text = "".join(td_tag.itertext()).strip()
            if td_text == "":
                continue
            if index == 1:
                lang_code = td_text
            elif index == 2:
                insert_data(conn, lang_code, td_text, WIKTIONARY_LANG_CODE)
                count += 1
    logger.info(f"Added {count} data from French Wiktionary")
