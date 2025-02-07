import re
from logging import Logger
from sqlite3 import Connection

from db import insert_data

WIKTIONARY_LANG_CODE = "th"


def extract_data_page(conn: Connection, page_number: str) -> int:
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://th.wiktionary.org/wiki/วิกิพจนานุกรม:รายชื่อภาษา/1
    # https://th.wiktionary.org/wiki/วิกิพจนานุกรม:รายชื่อภาษา/2
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": "วิกิพจนานุกรม:รายชื่อภาษา/" + page_number,
            "prop": "text",
            "disablelimitreport": "1",
        },
        ("parse", "text"),
    )
    root = etree.fromstring(page_html, etree.HTMLParser())
    count = 0
    for tr_tag in root.iterfind(".//table/tbody/tr"):
        lang_code = ""
        lang_name = ""
        other_names = ""
        for index, td_tag in enumerate(tr_tag.iterfind("td")):
            td_text = "".join(td_tag.itertext()).strip()
            match index:
                case 0:
                    lang_code = td_text
                case 1:
                    lang_name = td_text
                case 4:
                    other_names = td_text
        if (
            lang_code == ""
            or lang_name == ""
            or re.search(r"[A-Za-z]", lang_name) is not None
        ):
            continue
        insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
        count += 1
        for other_name in other_names.split(","):
            other_name = other_name.strip()
            if other_name == "" or re.search(r"[A-Za-z]", other_name) is not None:
                continue
            insert_data(conn, lang_code, other_name, WIKTIONARY_LANG_CODE, alt="other")
            count += 1
    return count


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    count = 0
    for page in ["1", "2"]:
        count += extract_data_page(conn, page)
    logger.info(f"Added {count} data from Thai Wiktionary")
