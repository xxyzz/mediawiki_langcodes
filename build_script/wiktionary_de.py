from sqlite3 import Connection

from db import insert_data

WIKTIONARY_LANG_CODE = "de"


def add_de_wiktionary_languages(conn: Connection) -> None:
    from xml.etree import ElementTree

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
            first_td_text = ""
            for index, td_tag in enumerate(tr_tag.iterfind("td")):
                td_text = "".join(td_tag.itertext()).strip()
                match index:
                    case 0:
                        first_td_text = td_text
                    case 1:
                        lang_code = td_text.strip("{}")
                    case 2:
                        insert_td_lang_data(conn, lang_code, td_text)
            insert_td_lang_data(conn, lang_code, first_td_text)

    for lang_code, lang_name in EXTRA_LANG_NAMES:
        insert_data(conn, lang_code, lang_name, WIKTIONARY_LANG_CODE)


def insert_td_lang_data(conn: Connection, lang_code: str, td_text: str) -> None:
    for lang_name in filter(None, td_text.split("/")):
        insert_data(conn, lang_code, lang_name.strip(), WIKTIONARY_LANG_CODE)


EXTRA_LANG_NAMES = (
    ("mul", "International"),
    ("pnb", "West-Pandschabi"),
    ("nhn", "Zentral-Nahuatl"),
    ("spx", "Südpikenisch"),
    ("de", "Frühneuhochdeutsch"),  # Early New High German, doesn't have ISO code
    ("xum", "Umbrisch"),
    ("xvo", "Volskisch"),
    ("ims", "Marsisch"),  # https://de.wikipedia.org/wiki/Marsische_Sprache
    ("xvs", "Vestinisch"),
    ("osc", "Oskisch"),
    ("jam", "Jamaika-Kreolisch"),  # https://en.wikipedia.org/wiki/Jamaican_Patois
    ("nhw", "Huastekisches West-Nahuatl"),  # Huasteca Nahuatl
    ("ote", "Mezquital-Otomi"),  # https://en.wikipedia.org/wiki/Northwestern_Otomi
    ("nhe", "Huastekisches Ost-Nahuatl"),  # Huastec Eastern Nahuatl
    ("nci", "Klassisches Nahuatl‎"),  # https://en.wikipedia.org/wiki/Classical_Nahuatl
    ("nhv", "Temascaltepec-Nahuatl"),
    ("nhg", "Tetelcingo-Nahuatl"),
    ("xae", "Äquisch"),
    ("nlv", "Orizaba-Nahuatl"),
    ("cs", "Alttschechisch"),
    ("qu", "Argentinisches Quechua"),
    ("hus", "Huastekisch"),
    ("grc", "Mittelgriechisch"),
    ("tkl", "Tokelauisch"),
    ("ncx", "Zentrales Puebla-Nahuatl"),
    ("ngu", "Guerrero-Nahuatl"),
    ("zai", "Isthmus-Zapotekisch"),
    ("odt", "Altniederländisch"),
    ("mrv", "Mangarevanisch"),
    ("umc", "Marrukinisch"),
    ("kj", "Oshivambo"),
    ("ota", "Osmanisches Türkisch"),
    ("pcd", "Pikardisch"),
    ("pkp", "Pukapuka"),
    ("mpm", "Yosondúa-Mixtekisch"),
)
