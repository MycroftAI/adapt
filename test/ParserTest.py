import unittest
import pprint

from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.parser import Parser
from adapt.entity_tagger import EntityTagger


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        self.tokenizer = EnglishTokenizer()
        self.regex_entities = []
        self.tagger = EntityTagger(self.trie, self.tokenizer, regex_entities=self.regex_entities)
        self.trie.insert("play", ("play", "PlayVerb"))
        self.trie.insert("the big bang theory", ("the big bang theory", "Television Show"))
        self.trie.insert("the big", ("the big", "Not a Thing"))
        self.trie.insert("barenaked ladies", ("barenaked ladies", "Radio Station"))
        self.trie.insert("show", ("show", "Command"))
        self.trie.insert("what", ("what", "Question"))
        self.parser = Parser(self.tokenizer, self.tagger)
        pass

    def test_basic_intent(self):
        s = "show play the big bang theory"
        verify = {'confidence': 0.9310344827586207,
                     'tags': [{'end_token': 0,
                               'entities': [{'confidence': 1.0,
                                             'data': [('show', 'Command')],
                                             'key': 'show',
                                             'match': 'show'}],
                               'from_context': False,
                               'key': 'show',
                               'match': 'show',
                               'start_token': 0},
                              {'end_token': 1,
                               'entities': [{'confidence': 1.0,
                                             'data': [('play', 'PlayVerb')],
                                             'key': 'play',
                                             'match': 'play'}],
                               'from_context': False,
                               'key': 'play',
                               'match': 'play',
                               'start_token': 1},
                              {'confidence': 1.0,
                               'end_token': 5,
                               'entities': [{'confidence': 1.0,
                                             'data': [('the big bang theory',
                                                       'Television Show')],
                                             'key': 'the big bang theory',
                                             'match': 'the big bang theory'}],
                               'from_context': False,
                               'key': 'the big bang theory',
                               'match': 'the big bang theory',
                               'start_token': 2}],
                     'time': 0.0001361370086669922,
                     'utterance': 'show play the big bang theory'}
        for result in self.parser.parse(s):
            assert ( result['tags'] == verify['tags'] )

if __name__ == '__main__':
    unittest.main()
