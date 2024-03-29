from unittest import TestCase

from mediawiki_langcodes import code_to_name


class TestCodeToName(TestCase):
    def test_antonym(self) -> None:
        self.assertEqual(code_to_name("en"), "English")

    def test_in_language(self) -> None:
        self.assertEqual(code_to_name("en", "zh"), "英语")

    def test_mediawiki_name(self) -> None:
        """
        'Qafár af' is defined in MediaWiki code, 'Qafar' is added from cldr
        """
        self.assertEqual(code_to_name("aa"), "Qafár af")

    def test_no_empty_str(self) -> None:
        import sqlite3

        from mediawiki_langcodes.convert import DB_PATH

        conn = sqlite3.connect(str(DB_PATH))
        empty_lang_name = 0
        empty_lang_code = 0
        for (empty_lang_code,) in conn.execute(
            "SELECT count(*) FROM langcodes WHERE lang_code = ''"
        ):
            pass
        for (empty_lang_name,) in conn.execute(
            "SELECT count(*) FROM langcodes WHERE lang_name = ''"
        ):
            pass
        conn.close()
        self.assertEqual(empty_lang_code, 0)
        self.assertEqual(empty_lang_name, 0)
