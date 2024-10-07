from logging import Logger
from sqlite3 import Connection

from db import insert_data

WIKTIONARY_LANG_CODE = "es"


def add_wiktionary_languages(conn: Connection, logger: Logger) -> None:
    from lxml import etree
    from mediawiki_api import mediawiki_api_request

    # https://es.wiktionary.org/wiki/Wikcionario:Códigos_de_idioma
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {"action": "parse", "page": "Wikcionario:Códigos de idioma", "prop": "text"},
        ("parse", "text"),
    )
    root = etree.fromstring(page_html, etree.HTMLParser())
    count = 0
    for header_tag in root.xpath(".//h3 | .//h4"):
        header_text = header_tag.xpath("string()")
        if header_text.startswith(
            (
                "Códigos de tres letras",  # tables under it are added by h4 tags
                "Códigos prohibidos",  # banned codes
            )
        ):
            continue
        for table_tag in header_tag.xpath(
            "parent::*/following-sibling::table[1]/tbody"
        ):
            for tr_tag in table_tag.iterfind(".//tr"):
                lang_code = ""
                for index, td_tag in enumerate(tr_tag.iterfind("td")):
                    td_text = td_tag.xpath("string()").strip()
                    match index:
                        case 0:
                            lang_code = td_text
                        case 1:
                            insert_data(conn, lang_code, td_text, WIKTIONARY_LANG_CODE)
                            count += 1
                        case 4:
                            for lang_name in td_text.split(", "):
                                lang_name = lang_name.strip()
                                if len(lang_name) > 0:
                                    insert_data(
                                        conn, lang_code, lang_name, WIKTIONARY_LANG_CODE
                                    )
                                    count += 1
    logger.info(f"Added {count} data from Spanish Wiktionary")
