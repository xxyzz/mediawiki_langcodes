import json
import sqlite3
from pathlib import Path

from db import insert_data


def add_extra_names(conn: sqlite3.Connection) -> None:
    """
    Add some extra language names used in Wiktionary language titles.
    """
    for json_path in Path("build_script/extra_names").iterdir():
        in_lang = json_path.stem
        with json_path.open(encoding="utf-8") as f:
            for lang_code, lang_names in json.load(f).items():
                lang_exists = lang_code_exists(conn, lang_code, in_lang)
                for index, lang_name in enumerate(lang_names):
                    insert_data(
                        conn,
                        lang_code,
                        lang_name,
                        in_lang,
                        f"extra{index}" if lang_exists else "",
                    )
                    lang_exists = True


def lang_code_exists(conn: sqlite3.Connection, lang_code: str, in_lang: str) -> bool:
    for _ in conn.execute(
        """
        SELECT lang_code
        FROM langcodes WHERE lang_code = ? AND in_lang = ? LIMIT 1
        """,
        (lang_code, in_lang),
    ):
        return True
    return False


if __name__ == "__main__":
    import argparse
    from collections import defaultdict

    from mediawiki_langcodes import name_to_code

    parser = argparse.ArgumentParser(description="Create extra language JSON file")
    parser.add_argument("in_lang", help="language code of the names language")
    parser.add_argument(
        "json_path", type=Path, help="language JSON file created from wikitextract"
    )
    args = parser.parse_args()

    extra_langs = defaultdict(list)
    with args.json_path.open(encoding="utf-8") as f:
        for lang_code, lang_names in json.load(f).items():
            for lang_name in lang_names:
                if name_to_code(lang_name, args.in_lang) != lang_code:
                    extra_langs[lang_code].append(lang_name)
    with open(
        f"build_script/extra_names/{args.in_lang}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(extra_langs, f, ensure_ascii=False, sort_keys=True, indent=2)
