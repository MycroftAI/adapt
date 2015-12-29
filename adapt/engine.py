import re
import pyee
from entity_tagger import EntityTagger
from parser import Parser
from tools.text.tokenizer import EnglishTokenizer
from tools.text.trie import Trie

__author__ = 'seanfitz'


class IntentDeterminationEngine(pyee.EventEmitter):
    def __init__(self, tokenizer=None, trie=None):
        pyee.EventEmitter.__init__(self)
        self.tokenizer = tokenizer or EnglishTokenizer()
        self.trie = trie or Trie()
        self.regular_expressions_entities = []
        self._regex_strings = set()
        self.tagger = EntityTagger(self.trie, self.tokenizer, self.regular_expressions_entities)
        self.intent_parsers = []

    def __best_intent(self, parse_result):
        best_intent = None
        for intent in self.intent_parsers:
            i = intent.validate(parse_result.get('tags'), parse_result.get('confidence'))
            if not best_intent or (i and i.get('confidence') > best_intent.get('confidence')):
                best_intent = i

        return best_intent

    def determine_intent(self, utterance, num_results=1):
        parser = Parser(self.tokenizer, self.tagger)
        parser.on('tagged_entities',
                  (lambda result:
                   self.emit("tagged_entities", result)))

        for result in parser.parse(utterance, N=num_results):
            self.emit("parse_result", result)
            best_intent = self.__best_intent(result)
            if best_intent and best_intent.get('confidence', 0.0) > 0:
                return best_intent

    def register_entity(self, entity_value, entity_type):
        self.trie.insert(entity_value.lower(), data=entity_type)
        self.trie.insert(entity_type.lower(), data='Concept')

    def register_regex_entity(self, regex_str):
        if regex_str and regex_str not in self._regex_strings:
            self._regex_strings.add(regex_str)
            self.regular_expressions_entities.append(re.compile(regex_str, re.IGNORECASE))

    def register_intent_parser(self, intent_parser):
        """
        "Enforce" the intent parser interface at registration time.
        :param intent_parser:
        :return: None
        :raises ValueError on invalid intent
        """
        if hasattr(intent_parser, 'validate') and callable(intent_parser.validate):
            self.intent_parsers.append(intent_parser)
        else:
            raise ValueError("%s is not an intent parser" % str(intent_parser))
