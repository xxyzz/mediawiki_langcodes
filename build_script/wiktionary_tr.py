from logging import Logger
from sqlite3 import Connection

from db import insert_data

WIKTIONARY_LANG_CODE = "tr"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://tr.wiktionary.org/wiki/Vikisözlük:Diller_listesi
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "Vikisözlük:Diller_listesi",
            "prop": "text",
            "disablelimitreport": "1",
        },
        ("parse", "text"),
    )
    root = etree.fromstring(page_html, etree.HTMLParser())
    count = 0
    for tr_tag in root.iterfind(".//tbody/tr"):
        lang_code = ""
        lang_names = []
        for index, td_tag in enumerate(tr_tag.iterfind("td")):
            td_text = "".join(td_tag.itertext()).strip()
            match index:
                case 0 | 2:
                    lang_names.append(td_text)
                case 1:
                    lang_code = td_text
        if lang_code in ["", "??"]:
            continue
        for lang_name in lang_names:
            if (
                lang_name == ""
                or "/" in lang_name
                or "(" in lang_name
                or lang_name.startswith("Şablon:")
            ):
                continue
            insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
            count += 1
    logger.info(f"Added {count} data from Turkish Wiktionary")
