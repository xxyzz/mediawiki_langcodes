from unittest import TestCase

from mediawiki_langcodes import name_to_code


class TestNameToCode(TestCase):
    def test_only_code_name(self) -> None:
        self.assertEqual(name_to_code("English"), "en")

    def test_with_code_of_name(self) -> None:
        self.assertEqual(name_to_code("English", "en"), "en")