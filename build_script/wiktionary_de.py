from sqlite3 import Connection

WIKTIONARY_LANG_CODE = "de"


def add_de_wiktionary_languages(conn: Connection) -> None:
    from xml.etree import ElementTree

    from db import insert_data
    from mediawiki_api import mediawiki_api_request

    # https://de.wiktionary.org/wiki/Hilfe:Sprachkürzel
    page_html = mediawiki_api_request(
        WIKTIONARY_LANG_CODE,
        {"action": "parse", "page": "Hilfe:Sprachkürzel", "prop": "text"},
        ("parse", "text"),
    )
    root = ElementTree.fromstring(page_html)
    # use class name to filter first letter index table
    for table in root.iterfind(".//table[@class='wikitable']"):
        for tr_tag in table.iterfind(".//tr"):
            lang_code = ""
            for index, td_tag in enumerate(tr_tag.iterfind("td")):
                if index == 1:
                    lang_code = "".join(td_tag.itertext()).strip("{}")
                elif index == 2:
                    lang_name_str = "".join(td_tag.itertext()).strip()
                    for lang_name in lang_name_str.split("/"):
                        insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)
