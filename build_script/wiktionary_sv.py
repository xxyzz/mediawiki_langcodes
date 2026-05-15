from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "sv"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from db import insert_data
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://sv.wiktionary.org/wiki/Wiktionary:Stilguide/Språknamn
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "Wiktionary:Stilguide/Språknamn",
            "prop": "text",
            "disablelimitreport": "1",
        },
        ("parse", "text"),
    )
    root = etree.fromstring(page_html, etree.HTMLParser())
    count = 0
    for span in root.xpath(".//tbody//ul/li/span[@data-lang-name and @data-lang-code]"):
        lang_name = span.get("data-lang-name")
        lang_code = span.get("data-lang-code")
        if lang_code == "--":
            lang_code = "mul"
        insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
        count += 1
    logger.info(f"Added {count} data from Swedish Wiktionary")
