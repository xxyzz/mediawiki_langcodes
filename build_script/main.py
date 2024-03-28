from pathlib import Path

from db import create_index, init_db
from extract_cldr import extract_cldr
from extract_mediawiki import extract_mediawiki, extract_mediawiki_cldr
from wiktionary_de import add_de_wiktionary_languages
from wiktionary_en import add_en_wiktionary_languages
from wiktionary_zh import add_zh_wiktionary_languages


def main() -> None:
    db_path = Path("src") / "mediawiki_langcodes" / "langcodes.db"
    conn = init_db(db_path)
    extract_cldr(conn)
    extract_mediawiki_cldr(conn)
    extract_mediawiki(conn)
    add_en_wiktionary_languages(conn)
    add_de_wiktionary_languages(conn)
    add_zh_wiktionary_languages(conn)
    create_index(conn)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
