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

    # prefer to use name defined in MediaWiki
    in_lang_query = """
    SELECT lang_name FROM langcodes
    WHERE lang_code = :lang_code AND in_lang = :in_lang AND alt = 'mediawiki'
    UNION ALL
    SELECT lang_name FROM langcodes
    WHERE lang_code = :lang_code AND in_lang = :in_lang AND alt = ''
    LIMIT 1
    """

    conn = sqlite3.connect(str(DB_PATH))
    lang_name = ""
    for (result_name,) in conn.execute(
        in_lang_query, {"lang_code": lang_code, "in_lang": in_language}
    ):
        lang_name = result_name
    if lang_name == "" and "-" in in_language:
        # remove script and territory code
        for (result_name,) in conn.execute(
            in_lang_query,
            {"lang_code": lang_code, "in_lang": in_language.split("-", 1)[0]},
        ):
            lang_name = result_name
    if lang_name == "":
        for (result_name,) in conn.execute(
            """
            SELECT lang_name FROM langcodes
            WHERE lang_code = :lang_code AND alt = 'mediawiki'
            UNION ALL
            SELECT lang_name FROM langcodes
            WHERE lang_code = :lang_code AND alt = ''
            LIMIT 1
            """,
            {"lang_code": lang_code},
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
    lang_name = lang_name.lower()
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
    return lang_code.lower()


def get_all_names(
    in_language: str = "", only_defined: bool = False
) -> Iterator[Tuple[str, str]]:
    """
    Return tuple of language code and name.
    Only return language codes defined in MediaWiki if `only_defined` is `True`.
    """
    conn = sqlite3.connect(str(DB_PATH))
    sql_query = "SELECT lang_code, lang_name FROM langcodes"
    query_vars = []
    if only_defined:
        sql_query += " WHERE alt = 'mediawiki'"
    elif in_language == "":
        sql_query += " WHERE in_lang = lang_code"
    else:
        sql_query += " WHERE in_lang = ?"
        query_vars.append(in_language)

    for lang_code, lang_name in conn.execute(sql_query, tuple(query_vars)):
        if in_language != "" and only_defined:
            lang_name = code_to_name(lang_code, in_language)
        yield lang_code.lower(), lang_name
    conn.close()
