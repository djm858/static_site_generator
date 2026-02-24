import unittest

from html import extract_title


class TestHTML(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
what
test

## nope
# Hello

asd
"""
        self.assertEqual(extract_title(markdown), 'Hello')
