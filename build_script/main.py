from pathlib import Path

from add_extra import add_extra_names
from db import init_db
from extract_cldr import extract_cldr
from extract_mediawiki import extract_mediawiki, extract_mediawiki_cldr


def main() -> None:
    db_path = Path("src") / "mediawiki_langcodes" / "langcodes.db"
    conn = init_db(db_path)
    extract_cldr(conn)
    extract_mediawiki_cldr(conn)
    extract_mediawiki(conn)
    add_extra_names(conn)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
