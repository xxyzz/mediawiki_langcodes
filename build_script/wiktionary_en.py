from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "en"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from xml.etree import ElementTree

    from db import insert_data
    from mediawiki_api import mediawiki_api_request

    # https://en.wiktionary.org/wiki/Wiktionary:List_of_languages
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {"action": "parse", "page": "Wiktionary:List_of_languages", "prop": "text"},
        ("parse", "text"),
    )
    root = ElementTree.fromstring(page_html)
    count = 0
    for table in root.iterfind(".//table"):
        for tr_tag in table.iterfind(".//tr"):
            lang_code = ""
            for index, td_tag in enumerate(tr_tag.iterfind("td")):
                td_text = "".join(td_tag.itertext()).strip()
                if len(td_text) == 0:
                    continue
                if index == 0:
                    lang_code = td_text
                elif index == 1:  # canonical name
                    insert_data(conn, lang_code, td_text, WIKTIONARY_LANG_CODE)
                    count += 1
                elif index == 4:
                    for other_name in filter(None, td_text.split(", ")):
                        insert_data(conn, lang_code, other_name, WIKTIONARY_LANG_CODE)
                        count += 1
    logger.info(f"Added {count} data from English Wiktionary")
