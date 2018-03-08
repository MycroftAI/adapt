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

    def test_start_end_token_match_when_sorting_tagged_entities(self):
        repro_payload = [{"end_token": 1, "key": "1", "entities": [{"key": "1", "data": [["1", "Which"]], "confidence": 0.5, "match": "1"}], "start_token": 1, "match": "1"}, {"end_token": 1, "key": "1", "entities": [{"key": "1", "data": [["1", "Which"]], "confidence": 0.5, "match": "1"}], "start_token": 1, "match": "1"}, {"end_token": 1, "key": "1", "entities": [{"key": "1", "data": [["1", "Which"]], "confidence": 0.5, "match": "1"}], "start_token": 1, "match": "1"}, {"end_token": 1, "key": "1", "entities": [{"key": "1", "data": [["1", "Which"]], "confidence": 0.5, "match": "1"}], "start_token": 1, "match": "1"}, {"end_token": 3, "key": "20", "entities": [{"key": "20", "data": [["20", "SnoozeTime"]], "confidence": 0.5, "match": "20"}], "start_token": 3, "match": "20"}, {"end_token": 4, "key": "20 minutes", "entities": [{"key": "20 minutes", "data": [["20 minutes", "SnoozeTime"]], "confidence": 0.5, "match": "20 minutes"}], "start_token": 3, "match": "20 minutes"}, {"end_token": 3, "key": "20", "entities": [{"key": "20", "data": [["20", "Which"]], "confidence": 0.5, "match": "20"}], "start_token": 3, "match": "20"}, {"end_token": 3, "key": "20", "entities": [{"key": "20", "data": [["20", "Which"]], "confidence": 0.5, "match": "20"}], "start_token": 3, "match": "20"}, {"end_token": 0, "key": "snooze", "entities": [{"key": "snooze", "data": [["snooze", "SnoozeKeyword"]], "confidence": 1.0, "match": "snooze"}], "start_token": 0, "match": "snooze"}, {"end_token": 2, "key": "for", "entities": [{"key": "for", "data": [["for", "SnoozeFiller"]], "confidence": 1.0, "match": "for"}], "start_token": 2, "match": "for"}]
        # just asserting that the sort does not crash in py3
        self.tagger._sort_and_merge_tags(repro_payload)

