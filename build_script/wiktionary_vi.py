from logging import Logger
from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "vi"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    import string

    count = extract_page(conn, None)
    for index in string.ascii_uppercase:
        count += extract_page(conn, index)
    logger.info(f"Added {count} data from Vietnamese Wiktionary")


def extract_page(conn: Connection, index: str | None) -> int:
    from db import insert_data
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://vi.wiktionary.org/wiki/Wiktionary:Danh_sách_ngôn_ngữ
    page_title = (
        "Wiktionary:Danh_sách_ngôn_ngữ"
        if index is None
        else f"Wiktionary:Danh_sách_ngôn_ngữ/{index}"
    )
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {
            "action": "parse",
            "page": page_title,
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
                    a_node = td.find("a")
                    if a_node is not None and (
                        lang_name.startswith("tiếng ")
                        or not a_node.get("class", "") == "new"
                    ):
                        insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
                    count += 1
                case _:
                    break
    return count
