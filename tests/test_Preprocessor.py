import unittest
from semantic_search.Preprocessor import Preprocessor


class test_Preprocessor(unittest.TestCase):

    def setup(self):
        pass

    def test_init(self):
        config = {'LOWER': False}
        preprocessor = Preprocessor(config)
        self.assertFalse(preprocessor.LOWER)
        self.assertFalse(hasattr(preprocessor, 'RM_NUMBERS'))

        config = {'LOWER': False, 'RM_NUMBERS': True}
        preprocessor = Preprocessor(config)
        self.assertFalse(preprocessor.LOWER)
        self.assertTrue(preprocessor.RM_NUMBERS)

    def test_replaceNewlines(self):
        config = {'REPLACE_LINEBREAKS': True}
        preprocessor = Preprocessor(config)
        self.assertTrue(preprocessor.REPLACE_LINEBREAKS)
        text = 'replace linebreaks at the end of a line\nwith a whitespace\nand double linebreaks\n\n with a single one.\n\n'
        target = 'replace linebreaks at the end of a line with a whitespace and double linebreaks\n with a single one.\n'
        processed_text = preprocessor.replace_linebreaks(text)
        self.assertEqual(processed_text, target)

