import unittest
from adapt.parser import Parser
from adapt.entity_tagger import EntityTagger
from adapt.intent import IntentBuilder
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie

__author__ = 'seanfitz'


class IntentTest(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()
        self.tokenizer = EnglishTokenizer()
        self.tagger = EntityTagger(self.trie, self.tokenizer)
        self.trie.insert("play", "PlayVerb")
        self.trie.insert("the big bang theory", "Television Show")
        self.trie.insert("the big", "Not a Thing")
        self.trie.insert("barenaked ladies", "Radio Station")
        self.parser = Parser(self.tokenizer, self.tagger)

    def tearDown(self):
        pass

    def test_basic_intent(self):
        intent = IntentBuilder("play television intent")\
            .require("PlayVerb")\
            .require("Television Show")\
            .build()
        for result in self.parser.parse("play the big bang theory"):
            result_intent = intent.validate(result.get('tags'), result.get('confidence'))
            assert result_intent.get('confidence') > 0.0
            assert result_intent.get('PlayVerb') == 'play'
            assert result_intent.get('Television Show') == "the big bang theory"

    def test_at_least_one(self):
        intent = IntentBuilder("play intent")\
            .require("PlayVerb")\
            .one_of("Television Show", "Radio Station")\
            .build()
        for result in self.parser.parse("play the big bang theory"):
            result_intent = intent.validate(result.get('tags'), result.get('confidence'))
            assert result_intent.get('confidence') > 0.0
            assert result_intent.get('PlayVerb') == 'play'
            assert result_intent.get('Television Show') == "the big bang theory"

        for result in self.parser.parse("play the barenaked ladies"):
            result_intent = intent.validate(result.get('tags'), result.get('confidence'))
            assert result_intent.get('confidence') > 0.0
            assert result_intent.get('PlayVerb') == 'play'
            assert result_intent.get('Radio Station') == "barenaked ladies"

    def test_basic_intent_with_alternate_names(self):
        intent = IntentBuilder("play television intent")\
            .require("PlayVerb", "Play Verb")\
            .require("Television Show", "series")\
            .build()
        for result in self.parser.parse("play the big bang theory"):
            result_intent = intent.validate(result.get('tags'), result.get('confidence'))
            assert result_intent.get('confidence') > 0.0
            assert result_intent.get('Play Verb') == 'play'
            assert result_intent.get('series') == "the big bang theory"
