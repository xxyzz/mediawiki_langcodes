import json
import sqlite3
from pathlib import Path

from db import insert_data


def add_extra_names(conn: sqlite3.Connection) -> None:
    """
    Add some extra language names used in Wiktionary language titles.
    """

    for json_path in Path("build_script/extra_names").iterdir():
        code_of_name = json_path.stem
        with json_path.open(encoding="utf-8") as f:
            for lang_code, lang_names in json.load(f).items():
                for index, lang_name in enumerate(lang_names):
                    insert_data(
                        conn, lang_code, lang_name, code_of_name, f"extra{index}"
                    )
