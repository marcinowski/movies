import unittest
from .parser import OMDBTranslator


class TestOMDBParser(unittest.TestCase):
    def setUp(self):
        pass


class TestParser(unittest.TestCase):
    def setUp(self):
        self.data = {
            'Plot': 'Test plot',
            'Writer': 'Adam Test',
            'Year': 1560,
        }
        self.parser = OMDBTranslator(self.data)

    def test_translate(self):
        response = self.parser.translate()
        expected = {
            'description': 'Test plot',
            'year': 1560,
        }
        self.assertEqual(response, expected)
