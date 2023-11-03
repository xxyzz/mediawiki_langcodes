import sys
import sqlite3


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

    conn = sqlite3.connect(DB_PATH)
    lang_name = ""
    for (result_name,) in conn.execute(
        "SELECT lang_name FROM langcodes WHERE lang_code = ? AND code_of_name = ? AND alt == '' LIMIT 1",
        (lang_code, in_language),
    ):
        lang_name = result_name
    if lang_name == "" and "-" in in_language:
        # remove script and territory code
        for (result_name,) in conn.execute(
            "SELECT lang_name FROM langcodes WHERE lang_code = ? AND code_of_name = ? AND alt == '' LIMIT 1",
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


def name_to_code(lang_name: str) -> str:
    """
    Return empty string if `lang_name` doesn't exists.
    """
    conn = sqlite3.connect(DB_PATH)
    lang_code = ""
    for (result_code,) in conn.execute(
        "SELECT lang_code FROM langcodes WHERE lang_name = ? LIMIT 1", (lang_name,)
    ):
        lang_code = result_code

    conn.close()
    return lang_code
