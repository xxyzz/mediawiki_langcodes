import xml.etree.ElementTree as ET
from pathlib import Path
from sqlite3 import Connection

from db import insert_data


def extract_cldr(conn: Connection) -> None:
    for path in Path("build").glob("cldr-*"):
        cldr_path = path
        break
    for xml_path in (cldr_path / "common" / "main").iterdir():
        tree = ET.parse(xml_path)
        root = tree.getroot()
        language_node = root.find("identity/language")
        if language_node is None:
            continue
        in_lang = language_node.get("type", "")
        script_node = root.find("identity/script")
        if script_node is not None:
            in_lang += "-"
            in_lang += script_node.get("type", "")
        territory_node = root.find("identity/territory")
        if territory_node is not None:
            in_lang += "-"
            in_lang += territory_node.get("type", "")

        for lang_node in root.findall("localeDisplayNames/languages/language"):
            lang_name = lang_node.text
            if lang_name == "↑↑↑":
                continue
            insert_data(
                conn,
                lang_node.get("type", ""),
                lang_name or "",
                in_lang,
                lang_node.get("alt", ""),
            )
