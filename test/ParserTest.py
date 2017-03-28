import unittest

from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.parser import Parser
from adapt.entity_tagger import EntityTagger


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.regular_expressions_entities = []
        self.trie = Trie()
        self.tokenizer = EnglishTokenizer()
        self.tagger = EntityTagger(self.trie, self.tokenizer, self.regular_expressions_entities)
        self.parser = Parser(self.tokenizer, self.tagger)
        pass

if __name__ == '__main__':
    unittest.main()
