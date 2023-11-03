import logging
from pathlib import Path

from db import init_db
from download_files import download_files
from extract_cldr import extract_cldr
from extract_mediawiki import extract_mediawiki, extract_mediawiki_cldr


def main() -> None:
    download_files()
    db_path = Path("src") / "mediawiki_langcodes" / "langcodes.db"
    conn = init_db(db_path)
    extract_cldr(conn)
    extract_mediawiki_cldr(conn)
    extract_mediawiki(conn)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )
    main()
