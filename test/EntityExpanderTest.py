from adapt.entity_tagger import EntityTagger
from adapt.expander import BronKerboschExpander
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie

__author__ = 'seanfitz'

import unittest


class BronKerboschExpanderTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = EnglishTokenizer()
        self.trie = Trie(max_edit_distance=2)
        self.trie.insert("x-play", "Television Show")
        self.trie.insert("play", "Play Verb")
        self.trie.insert("play season", "Time Period")
        self.trie.insert("play", "Player Control")
        self.trie.insert("season", "Season Prefix")
        self.trie.insert("1", "Number")
        self.trie.insert("the big bang theory", "Television Show")
        self.trie.insert("the big", "Television Show")
        self.trie.insert("big bang", "event")
        self.trie.insert("bang theory", "Scientific Theory")
        self.tagger = EntityTagger(self.trie, self.tokenizer)

    def testExpander(self):
        self.tagger.trie.max_edit_distance = 0
        tags = self.tagger.tag("play season 1 of the big bang theory")
        expander = BronKerboschExpander(self.tokenizer)
        parse_results = list(expander.expand(tags))
        assert len(parse_results) == 6

    def testExpandedResult(self):
        tags = self.tagger.tag("season 1")
        expander = BronKerboschExpander(self.tokenizer)
        parse_results = list(expander.expand(tags))
        assert len(parse_results) == 1
        assert len(parse_results[0]) == 2


    def testConsistentExpandWithSameOverlapMultipleTimes(self):
        """
        example: play season 1 of the big bang theory play season one of the big bang theory
        series should contain two instances of the big bang theory
        :return:
        """
        utterance = "play season 1 of the big bang theory"
        tags = self.tagger.tag(utterance)

        def score_clique(clique):
            score = 0.0
            for tagged_entity in clique:
                ec = tagged_entity.get('entities', [{'confidence': 0.0}])[0].get('confidence')
                score += ec * len(tagged_entity.get('entities', [{'match': ''}])[0].get('match')) / (
                    len(utterance) + 1)
            return score
        expander = BronKerboschExpander(self.tokenizer)
        parse_results = list(expander.expand(tags, clique_scoring_func=score_clique))
        assert len(parse_results) == 6
        result_text = ' '.join([tag.get('entities')[0].get('key') for tag in parse_results[0]])
        result_parse = ', '.join(
            [tag.get('entities')[0].get('data')[0][1] for tag in parse_results[0]]
        )

        assert result_text == 'play season 1 the big bang theory'

    def testExpandWithRegexAndLiteralTokenMatch(self):
        # two tags for the same token, different confidence, should expand to two cliques
        tags = [{'end_token': 0, 'start_token': 0, 'key': u'spell', 'match': u'spell',
                 'entities': [{'confidence': 0.5, 'data': [u'SearchTerms'], 'match': u'spell', 'key': u'spell'}]},
                {'end_token': 0, 'start_token': 0, 'key': u'spell', 'match': u'spell',
                 'entities': [{'confidence': 1.0, 'data': [u'SpellingKeyword'], 'match': u'spell', 'key': u'spell'}]}]

        expander = BronKerboschExpander(self.tokenizer)

        cliques = list(expander._sub_expand(tags))
        assert len(cliques) == 2