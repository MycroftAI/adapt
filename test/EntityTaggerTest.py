import unittest
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
import re

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

    def test_regex_tag(self):
        regex = re.compile(r"the (?P<Event>\w+\s\w+) theory")
        tagger = EntityTagger(self.trie, EnglishTokenizer(), regex_entities=[regex])
        tags = tagger.tag("the big bang theory")
        assert len(tags) == 3
        event_tags = [tag for tag in tags if tag.get('match') == 'big bang']
        assert len(event_tags) == 1
        assert len(event_tags[0].get('entities')) == 1
        assert len(event_tags[0].get('entities')[0].get('data')) == 1
        assert ('big bang', 'Event') in event_tags[0].get('entities')[0].get('data')
