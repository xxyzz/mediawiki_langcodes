import json
import shutil
import subprocess
from pathlib import Path
from sqlite3 import Connection
from tempfile import NamedTemporaryFile

from db import insert_data


def extract_data_from_php_file(
    conn: Connection,
    php_path: Path,
    php_code: str,
    in_lang: str | None,
    from_mediawiki: bool,
) -> None:
    with (
        php_path.open(encoding="utf-8") as php_f,
        NamedTemporaryFile("w+", encoding="utf-8") as temp_f,
    ):
        shutil.copyfileobj(php_f, temp_f)
        temp_f.write(php_code)
        temp_f.flush()
        subp = subprocess.run(["php", temp_f.name], capture_output=True, text=True)
        if len(subp.stdout) > 0:
            languages = json.loads(subp.stdout)
            for lang_code, lang_name in languages.items():
                insert_data(
                    conn,
                    lang_code,
                    lang_name,
                    in_lang or lang_code,
                    "mediawiki" if from_mediawiki else "",
                )


def extract_mediawiki(conn: Connection) -> None:
    # https://github.com/wikimedia/mediawiki/blob/master/includes/languages/data/Names.php
    for path in Path("build").glob("mediawiki-1.*"):
        mediawiki_path = path
        break
    php_path = mediawiki_path / "includes" / "languages" / "data" / "Names.php"
    extract_data_from_php_file(
        conn, php_path, "echo json_encode(Names::$names);", None, True
    )


def extract_mediawiki_cldr(conn: Connection) -> None:
    # https://github.com/wikimedia/mediawiki-extensions-cldr/tree/master/LocalNames
    for path in Path("build").glob("mediawiki-extensions-cldr-*"):
        repo_path = path
        break
    for php_path in (repo_path / "LocalNames").iterdir():
        code_for_name = php_path.stem.removeprefix("LocalNames").lower()
        with php_path.open(encoding="utf-8") as f:
            # skip LocalNames/LocalNamesKk.php that only has `require_once`
            if "require_once" in f.read():
                continue

        extract_data_from_php_file(
            conn,
            php_path,
            """
            if (isset($languageNames)) {
                echo json_encode($languageNames);
            }
            """,
            code_for_name,
            False,
        )
