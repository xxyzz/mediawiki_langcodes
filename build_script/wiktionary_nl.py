from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "nl"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from db import insert_data
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    overrides = {
        "bem": "Bemba",
        "luo": "Luo",
    }

    # https://nl.wiktionary.org/wiki/WikiWoordenboek:ISO_639/totaal
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "WikiWoordenboek:ISO_639/totaal",
            "prop": "text",
            "disablelimitreport": "1",
        },
        ("parse", "text"),
    )
    root = etree.fromstring(page_html, etree.HTMLParser())
    count = 0
    for tr_tag in root.iterfind(".//tbody/tr"):
        lang_name = ""
        lang_code = ""
        for index, td_tag in enumerate(tr_tag.iterfind("td")):
            td_text = "".join(td_tag.itertext()).strip()
            if td_text == "":
                continue
            if index == 0:
                lang_name = td_text
            elif index == 1:
                lang_code = td_text
            elif index == 3:
                if lang_code == "":
                    lang_code = td_text
                if lang_code in overrides:
                    lang_name = overrides[lang_code]
                insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
                count += 1
    logger.info(f"Added {count} data from Dutch Wiktionary")
