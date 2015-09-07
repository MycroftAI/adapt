import unittest
from entity_tagger import EntityTagger
from tools.text.tokenizer import EnglishTokenizer
from tools.text.trie import Trie

__author__ = 'seanfitz'


class EntityTaggerTest(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()
        self.tagger = EntityTagger(self.trie, EnglishTokenizer())
        self.trie.insert("play", "PlayVerb")
        self.trie.insert("the big bang theory", "Television Show")
        self.trie.insert("the big", "Not a Thing")

    def tearDown(self):
        pass

    def test_tag(self):
        tags = list(self.tagger.tag("play season 1 of the big bang theory"))
        assert len(tags) == 3
