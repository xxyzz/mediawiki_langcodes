from unittest import TestCase

from mediawiki_langcodes import get_all_names


class TestAllNames(TestCase):
    def test_get_all_names(self) -> None:
        names = list(get_all_names())
        self.assertGreater(len(names), 0)

    def test_get_all_names_in_en(self) -> None:
        names = list(get_all_names("en"))
        self.assertGreater(len(names), 0)

    def test_mediawiki_defined(self) -> None:
        autonym_codes = {lang_code for lang_code, _ in get_all_names(only_defined=True)}
        fr_codes = [lang_code for lang_code, _ in get_all_names("fr", True)]
        fr_code_set = set(fr_codes)
        self.assertEqual(len(fr_code_set), len(fr_codes))
        self.assertEqual(len(fr_code_set), len(autonym_codes))
        self.assertEqual(autonym_codes, fr_code_set)
