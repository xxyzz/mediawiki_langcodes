from unittest import TestCase

from mediawiki_langcodes import code_to_name, get_all_names


class TestCodeToName(TestCase):
    def test_antonym(self) -> None:
        self.assertEqual(code_to_name("en"), "English")

    def test_in_language(self) -> None:
        self.assertEqual(code_to_name("en", "zh"), "英语")

    def test_get_all_names(self) -> None:
        names = list(get_all_names())
        self.assertGreater(len(names), 0)

    def test_get_all_names_in_en(self) -> None:
        names = list(get_all_names("en"))
        self.assertGreater(len(names), 0)
