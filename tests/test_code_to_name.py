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
