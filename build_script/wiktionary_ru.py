from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "ru"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from db import insert_data
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://ru.wiktionary.org/wiki/Викисловарь:Статистика
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "Викисловарь:Статистика",
            "prop": "text",
            "disablelimitreport": "1",
        },
        ("parse", "text"),
    )
    root = etree.fromstring(page_html, etree.HTMLParser())
    count = 0
    for tr in root.iterfind(".//tbody/tr"):
        for index, td in enumerate(tr.iterfind("td")):
            if index == 1:
                span = td.find("span")
                a = td.find("a")
                if span is None or a is None:
                    break
                lang_code = "".join(span.itertext()).strip()
                lang_name = "".join(a.itertext()).strip()
                insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
                count += 1
    logger.info(f"Added {count} data from Russian Wiktionary")

    EXTRA_LANG_NAMES = (
        ("orv", "Древнерусский"),
        ("ang", "Древнеанглийский"),
    )
    for lang_code, lang_name in EXTRA_LANG_NAMES:
        insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
