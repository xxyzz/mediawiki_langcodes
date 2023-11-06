from unittest import TestCase

from mediawiki_langcodes import name_to_code


class TestNameToCode(TestCase):
    def test_only_code_name(self) -> None:
        self.assertEqual(name_to_code("English"), "en")

    def test_in_lang(self) -> None:
        self.assertEqual(name_to_code("English", "en"), "en")

    def test_zh_extra(self) -> None:
        self.assertEqual(name_to_code("韓語"), "ko")
