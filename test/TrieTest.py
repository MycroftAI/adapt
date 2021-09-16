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
from adapt.tools.text.trie import Trie

__author__ = 'seanfitz'


class TrieTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_basic_retrieval(self):
        trie = Trie()
        trie.insert("restaurant")
        results = list(trie.lookup("restaurant"))
        assert len(results) == 1

    def test_data_is_correct_on_insert(self):
        trie = Trie()
        trie.insert("restaurant", "Concept")
        results = list(trie.lookup("restaurant"))
        assert len(results) == 1
        assert len(results[0].get('data')) == 1
        data = list(results[0].get('data'))
        assert data[0] == 'Concept'

    def test_gather(self):
        trie = Trie()
        trie.insert("rest")
        trie.insert("restaurant")
        results = list(trie.gather("restaurant"))
        assert len(results) == 1
        assert results[0].get('key') == "restaurant"

    def test_retrieval_based_on_insertion_order(self):
        trie = Trie()
        trie.insert("rest")
        trie.insert("restaurant")
        results = list(trie.lookup("rest"))
        assert len(results) == 1
        results = list(trie.lookup("restaurant"))
        assert len(results) == 1

    def test_retrieval_of_multi_word_entity(self):
        trie = Trie()
        trie.insert("play", "PlayVerb")
        trie.insert("the big bang theory", "Television Series")
        results = list(trie.gather("1 of the big bang theory"))
        assert len(results) == 0

    def test_insert_single_character_entity(self):
        trie = Trie()
        trie.insert("1", "Number")
        results = list(trie.gather("1 of the big bang theory"))
        assert len(results) == 1
        assert len(results[0].get('data')) == 1

    def test_simple_remove(self):
        trie = Trie()
        trie.insert("1", "Number")
        results = list(trie.lookup("1"))
        assert len(results) == 1
        assert len(results[0].get('data')) == 1

        assert trie.remove("1")
        results = list(trie.lookup("1"))
        assert len(results) == 0

    def test_named_remove(self):
        trie = Trie()
        trie.insert("1", "Number")
        trie.insert("1", "The Loneliest")
        results = list(trie.lookup("1"))
        assert len(results) == 1
        assert len(results[0].get('data')) == 2

        assert trie.remove("1", "Number")
        results = list(trie.lookup("1"))
        assert len(results) == 1
        assert len(results[0].get('data')) == 1

    def test_edit_distance(self):
        trie = Trie(max_edit_distance=1)
        trie.insert("restaurant")
        results = list(trie.lookup("restauran"))
        assert len(results) == 1
        results = list(trie.lookup("estaurant"))
        assert len(results) == 1
        results = list(trie.lookup("estauran"))
        assert len(results) == 0

    def test_edit_distance_confidence(self):
        trie = Trie(max_edit_distance=2)
        trie.insert("a")
        trie.insert("bb")
        trie.insert("ccc")
        trie.insert("dddd")
        trie.insert("100")
        results = list(trie.gather("b"))
        assert len(results) == 1
        assert results[0].get('confidence') == 0.5
        results = list(trie.gather("1 of"))
        assert len(results) == 3



    def test_edit_distance_no_confidence(self):
        trie = Trie(max_edit_distance=2)
        trie.insert("1", "Number")
        results = list(trie.gather("of the big bang theory"))
        assert len(results) == 0

    def test_remove(self):
        trie = Trie(max_edit_distance=2)
        trie.insert("1", "Number")
        trie.insert("2", "Number")
        trie.remove("2")

        one_lookup = list(trie.gather("1"))
        two_lookup = list(trie.gather("2"))
        assert len(one_lookup) == 1  # One match found
        assert len(two_lookup) == 0  # Zero matches since removed

    def test_remove_multi_last(self):
        trie = Trie(max_edit_distance=2)
        trie.insert("Kermit", "Muppets")
        trie.insert("Kermit", "Frogs")
        kermit_lookup = list(trie.lookup("Kermit"))[0]
        assert 'Frogs' in kermit_lookup['data']
        assert 'Muppets' in kermit_lookup['data']

        trie.remove("Kermit", "Frogs")

        kermit_lookup = list(trie.gather("Kermit"))[0]
        assert kermit_lookup['data'] == {"Muppets"}  # Right data remains

    def test_remove_multi_first(self):
        trie = Trie(max_edit_distance=2)
        trie.insert("Kermit", "Muppets")
        trie.insert("Kermit", "Frogs")
        kermit_lookup = list(trie.lookup("Kermit"))[0]
        assert 'Frogs' in kermit_lookup['data']
        assert 'Muppets' in kermit_lookup['data']

        trie.remove("Kermit", "Muppets")

        kermit_lookup = list(trie.lookup("Kermit"))[0]
        assert kermit_lookup['data'] == {"Frogs"}  # Right data remains

    def test_scan(self):
        trie = Trie(max_edit_distance=2)
        trie.insert("Kermit", "Muppets")
        trie.insert("Gonzo", "Muppets")
        trie.insert("Rowlf", "Muppets")
        trie.insert("Gobo", "Fraggles")

        def match_func(data):
            return data == "Muppets"

        results = trie.scan(match_func)
        assert len(results) == 3
        muppet_names = [r[0] for r in results]
        assert "Kermit" in muppet_names
        assert "Gonzo" in muppet_names
        assert "Rowlf" in muppet_names

    def test_is_prefix(self):
        trie = Trie()
        trie.insert("play", "PlayVerb")
        trie.insert("the big bang theory", "Television Show")
        trie.insert("the big", "Not a Thing")
        trie.insert("barenaked ladies", "Radio Station")

        assert trie.root.is_prefix("the")

    def tearDown(self):
        pass
