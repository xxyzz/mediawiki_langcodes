import sqlite3
import sys
from collections.abc import Iterator
from typing import Tuple

if sys.version_info < (3, 10):
    from importlib_resources import files
else:
    from importlib.resources import files


DB_PATH = files("mediawiki_langcodes") / "langcodes.db"


def code_to_name(lang_code: str, in_language: str = "") -> str:
    """
    Return autonym if `in_language` is not passed.
    Return empty string if `lang_code` doesn't exists.
    """
    if in_language == "":
        in_language = lang_code

    conn = sqlite3.connect(str(DB_PATH))
    lang_name = ""
    for (result_name,) in conn.execute(
        """
        SELECT lang_name FROM langcodes
        WHERE lang_code = ? AND in_lang = ? AND alt == ''
        LIMIT 1
        """,
        (lang_code, in_language),
    ):
        lang_name = result_name
    if lang_name == "" and "-" in in_language:
        # remove script and territory code
        for (result_name,) in conn.execute(
            """
            SELECT lang_name FROM langcodes
            WHERE lang_code = ? AND in_lang = ? AND alt == ''
            LIMIT 1
            """,
            (lang_code, in_language.split("-", 1)[0]),
        ):
            lang_name = result_name
    if lang_name == "":
        for (result_name,) in conn.execute(
            "SELECT lang_name FROM langcodes WHERE lang_code = ? AND alt == '' LIMIT 1",
            (lang_code,),
        ):
            lang_name = result_name

    conn.close()
    return lang_name


def name_to_code(
    lang_name: str, in_language: str = "", single_query: bool = False
) -> str:
    """
    Pass the language code of the language name to limit the search scope and reduce
    ambiguity.
    Return empty string if `lang_name` doesn't exists.
    """
    conn = sqlite3.connect(str(DB_PATH))
    lang_code = ""
    search_sql = "SELECT lang_code FROM langcodes WHERE lang_name = ?"
    search_values = [lang_name]
    if in_language != "":
        search_sql += " AND in_lang = ?"
        search_values.append(in_language)
    search_sql += " ORDER BY length(lang_code) LIMIT 1"
    for (result_code,) in conn.execute(search_sql, tuple(search_values)):
        lang_code = result_code
    conn.close()
    if in_language != "" and lang_code == "" and not single_query:
        lang_code = name_to_code(lang_name, single_query=True)
    return lang_code


def get_all_names(in_language: str = "") -> Iterator[Tuple[str, str]]:
    """
    Return tuple of language code and name.
    """
    conn = sqlite3.connect(str(DB_PATH))
    sql_query = "SELECT DISTINCT lang_code, lang_name FROM langcodes"
    query_values = []
    if in_language != "":
        sql_query += " WHERE in_lang = ?"
        query_values.append(in_language)
    else:
        sql_query += " WHERE lang_code = in_lang"
    for lang_code, lang_name in conn.execute(sql_query, tuple(query_values)):
        yield lang_code, lang_name
    conn.close()
