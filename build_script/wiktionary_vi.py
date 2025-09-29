from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "vi"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from db import insert_data
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://vi.wiktionary.org/wiki/Wiktionary:Danh_sách_ngôn_ngữ
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "Wiktionary:Danh_sách_ngôn_ngữ",
            "prop": "text",
            "disablelimitreport": "1",
        },
        ("parse", "text"),
    )
    root = etree.fromstring(page_html, etree.HTMLParser())
    count = 0
    tbody = root.xpath(".//table[contains(@class, 'wikitable')][1]/tbody")[0]
    for tr in tbody.iterfind("tr"):
        lang_code = ""
        for col_index, td in enumerate(tr.iterfind("td")):
            match col_index:
                case 0:
                    lang_code = "".join(td.itertext()).strip()
                case 1:
                    lang_name = "".join(td.itertext()).strip()
                    insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
                    count += 1
                case _:
                    break
    logger.info(f"Added {count} data from Vietnamese Wiktionary")
