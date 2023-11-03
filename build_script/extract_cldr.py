import xml.etree.ElementTree as ET
from pathlib import Path
from sqlite3 import Connection

from db import insert_data


def extract_cldr(conn: Connection) -> None:
    from download_files import GITHUB_REPO

    cldr_path = Path(f"build/cldr-{GITHUB_REPO['unicode-org/cldr']}")
    for xml_path in (cldr_path / "common" / "main").iterdir():
        tree = ET.parse(xml_path)
        root = tree.getroot()
        code_of_name = root.find("identity/language").get("type")
        script_node = root.find("identity/script")
        if script_node is not None:
            code_of_name += "-"
            code_of_name += script_node.get("type")
        territory_node = root.find("identity/territory")
        if territory_node is not None:
            code_of_name += "-"
            code_of_name += territory_node.get("type")

        for lang_node in root.findall("localeDisplayNames/languages/language"):
            lang_name = lang_node.text
            if lang_name == "↑↑↑":
                continue
            insert_data(
                conn,
                lang_node.get("type"),
                lang_name,
                code_of_name,
                lang_node.get("alt"),
            )
