import unittest
from adapt.tools.text.tokenizer import EnglishTokenizer

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = EnglishTokenizer()

    def test_basic_tokenizer(self):
        s = "hello, world, I'm a happy camper. I don't have any friends?"
        result = self.tokenizer.tokenize(s)
        assert (result == ['hello', ',', 'world', ',', 'I', "'m", 'a', 'happy', 'camper', '.', 'I', 'do', "n't", 'have', 'any', 'friends', '?'])
