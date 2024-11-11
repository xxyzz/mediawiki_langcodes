from logging import Logger
from sqlite3 import Connection

from db import insert_data

WIKTIONARY_LANG_CODE = "el"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://el.wiktionary.org/wiki/Βικιλεξικό:Πίνακας_γλωσσών
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "Βικιλεξικό:Πίνακας γλωσσών",
            "prop": "text",
            "disablelimitreport": "1",
        },
        ("parse", "text"),
    )
    root = etree.fromstring(page_html, etree.HTMLParser())
    count = 0
    tbody = root.find(".//table[@class='wikitable sortable']/tbody")
    for tr in tbody.iterfind("tr"):
        lang_name = ""
        lang_code = ""
        for index, td in enumerate(tr.iterfind("td")):
            if index == 0:
                lang_code = td.text.strip()
                if lang_code == "-":
                    break
            elif index == 2:
                lang_name = td.text.strip()
                insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
                count += 1
                break
    logger.info(f"Added {count} data from Greek Wiktionary")
