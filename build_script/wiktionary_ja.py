from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "ja"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from db import insert_data
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://ja.wiktionary.org/wiki/Wiktionary:言語名一貫性チェック
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "Wiktionary:言語名一貫性チェック",
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
            if td_tag.find("div") is not None:
                continue
            td_text = "".join(td_tag.itertext()).strip()
            if td_text == "":
                continue
            if index == 0:
                lang_code = td_text
            elif index == 1:
                insert_data(conn, lang_code, td_text, WIKTIONARY_LANG_CODE)
                count += 1
    logger.info(f"Added {count} data from Japanese Wiktionary")
