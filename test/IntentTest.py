# Copyright 2018 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
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
        self.regex_entities = []
        self.tagger = EntityTagger(self.trie, self.tokenizer, regex_entities=self.regex_entities)
        self.trie.insert("play", ("play", "PlayVerb"))
        self.trie.insert("the big bang theory", ("the big bang theory", "Television Show"))
        self.trie.insert("the big", ("the big", "Not a Thing"))
        self.trie.insert("barenaked ladies", ("barenaked ladies", "Radio Station"))
        self.trie.insert("show", ("show", "Command"))
        self.trie.insert("what", ("what", "Question"))
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

    def test_at_least_on_no_required(self):
        intent = IntentBuilder("play intent") \
            .one_of("Television Show", "Radio Station") \
            .build()
        for result in self.parser.parse("play the big bang theory"):
            result_intent = intent.validate(result.get('tags'), result.get('confidence'))
            assert result_intent.get('confidence') > 0.0
            assert result_intent.get('Television Show') == "the big bang theory"

        for result in self.parser.parse("play the barenaked ladies"):
            result_intent = intent.validate(result.get('tags'), result.get('confidence'))
            assert result_intent.get('confidence') > 0.0
            assert result_intent.get('Radio Station') == "barenaked ladies"

    def test_at_least_one_alone(self):
        intent = IntentBuilder("OptionsForLunch") \
            .one_of("Question", "Command") \
            .build()

        for result in self.parser.parse("show"):
            result_intent = intent.validate(result.get('tags'), result.get('confidence'))
            assert result_intent.get('confidence') > 0.0
            assert result_intent.get('Command') == "show"

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

    def test_intent_with_regex_entity(self):
        self.trie = Trie()
        self.tagger = EntityTagger(self.trie, self.tokenizer, self.regex_entities)
        self.parser = Parser(self.tokenizer, self.tagger)
        self.trie.insert("theory", ("theory", "Concept"))
        regex = re.compile(r"the (?P<Event>.*)")
        self.regex_entities.append(regex)
        intent = IntentBuilder("mock intent")\
            .require("Event")\
            .require("Concept").build()

        for result in self.parser.parse("the big bang theory"):
            result_intent = intent.validate(result.get('tags'), result.get('confidence'))
            assert result_intent.get('confidence') > 0.0
            assert result_intent.get('Event') == 'big bang'
            assert result_intent.get('Concept') == "theory"

    def test_intent_using_alias(self):
        self.trie.insert("big bang", ("the big bang theory", "Television Show"))
        intent = IntentBuilder("play television intent")\
            .require("PlayVerb", "Play Verb")\
            .require("Television Show", "series")\
            .build()
        for result in self.parser.parse("play the big bang theory"):
            result_intent = intent.validate(result.get('tags'), result.get('confidence'))
            assert result_intent.get('confidence') > 0.0
            assert result_intent.get('Play Verb') == 'play'
            assert result_intent.get('series') == "the big bang theory"

