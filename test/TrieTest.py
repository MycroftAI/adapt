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


    def tearDown(self):
        pass
