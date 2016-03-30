import unittest
from adapt.engine import DomainIntentDeterminationEngine
from adapt.intent import IntentBuilder

__author__ = 'seanfitz'


class DomainIntentDeterminationEngineTests(unittest.TestCase):
    """All tests related to the DomainIntentDeterminationEngine."""

    def setUp(self):
        """Setting up testing env."""
        self.engine = DomainIntentDeterminationEngine()

    def test_register_intent_parser(self):
        """Test to make sure that intent parser is working with correct data."""
        parser = IntentBuilder("Intent").build()
        self.engine.register_intent_parser(parser)
        self.assertEqual(len(self.engine.intent_parsers), 1)

    def test_register_intent_parser_defult_is_empty(self):
        """Test to make sure that the intent parser is empty when first created."""
        assert len(self.engine.intent_parsers) == 0

    def test_register_intent_parser_throws_error_if_not_intent_parsers(self):
        """
        Test register_intent_parser throws error if IntentBuilder object is not passed in.

        This should throw a ValueError.
        """
        with self.assertRaises(ValueError):
            self.engine.register_intent_parser("NOTAPARSER")

    def test_register_regex_entity(self):
        """Test to make sure a regex entity can be registered."""
        self.engine.register_regex_entity(".*")
        self.assertEqual(len(self.engine._regex_strings), 1)
        self.assertEqual(len(self.engine.regular_expressions_entities), 1)

    def test_register_regex_entity_default_is_empty(self):
        """Test to make sure that regex entity is empty by default."""
        self.assertEqual(len(self.engine._regex_strings), 0)
        self.assertEqual(len(self.engine.regular_expressions_entities), 0)

    def test_select_best_intent(self):
        """
        Test to make sure that best intent is being returned.

        This test is to make sure that best intent works identicly to its counter part
        in the IntentEngine.

        """
        parser1 = IntentBuilder("Parser1").require("Entity1").build()
        self.engine.register_intent_parser(parser1)
        self.engine.register_entity("tree", "Entity1")

        utterance = "go to the tree house"
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        self.assertEqual(intent['intent_type'], 'Parser1')

        parser2 = IntentBuilder("Parser2").require("Entity1").require("Entity2").build()
        self.engine.register_intent_parser(parser2)
        self.engine.register_entity("house", "Entity2")
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        self.assertEqual(intent['intent_type'], 'Parser2')

    def test_select_best_intent_with_domain(self):
        """Test to make sure that best intent is working with domains."""
        self.engine.register_domain('Domain1')
        self.engine.register_domain('Domain2')

        # Creating first intent domain
        parser1 = IntentBuilder("Parser1").require("Entity1").build()
        self.engine.register_intent_parser(parser1, domain='Domain1')
        self.engine.register_entity("tree", "Entity1", domain='Domain1')

        # Creating second intent domain
        parser2 = IntentBuilder("Parser2").require("Entity2").build()
        self.engine.register_intent_parser(parser2, domain="Domain2")
        self.engine.register_entity("house", "Entity2", domain="Domain2")

        utterance = "Entity1 Entity2 go to the tree house"
        intents = self.engine.determine_intent(utterance, 2)
        intent = next(intents)
        assert intent

        # confidence for Parser2 > Parser1
        self.assertEqual(intent['intent_type'], 'Parser2')

        intent = next(intents)
        assert intent
        self.assertEqual(intent['intent_type'], 'Parser1')
