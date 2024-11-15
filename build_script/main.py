def main() -> None:
    import importlib
    import logging
    from importlib.resources import files
    from pathlib import Path

    from db import count_rows, create_index, init_db
    from extract_cldr import extract_cldr
    from extract_mediawiki import extract_mediawiki, extract_mediawiki_cldr

    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
    logger = logging.getLogger("mediawiki_langcodes")
    logger.setLevel(logging.INFO)
    db_path = Path("src") / "mediawiki_langcodes" / "langcodes.db"
    conn = init_db(db_path)
    extract_cldr(conn, logger)
    extract_mediawiki_cldr(conn, logger)
    extract_mediawiki(conn, logger)
    create_index(conn)
    for code_path in files("main").glob("wiktionary_*.py"):  # type:ignore
        module = importlib.import_module(code_path.stem)
        module.add_wiktionary_languages(conn, logger)
    conn.commit()
    logger.info(f"Total rows: {count_rows(conn)}")
    conn.execute("PRAGMA optimize")
    conn.close()


if __name__ == "__main__":
    main()
