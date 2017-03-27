import unittest
from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder

__author__ = 'seanfitz'


class IntentEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = IntentDeterminationEngine()

    def testRegisterIntentParser(self):
        assert len(self.engine.intent_parsers) == 0
        try:
            self.engine.register_intent_parser("NOTAPARSER")
            assert "Did not fail to register invalid intent parser" and False
        except ValueError as e:
            pass
        parser = IntentBuilder("Intent").build()
        self.engine.register_intent_parser(parser)
        assert len(self.engine.intent_parsers) == 1

    def testRegisterRegexEntity(self):
        assert len(self.engine._regex_strings) == 0
        assert len(self.engine.regular_expressions_entities) == 0
        self.engine.register_regex_entity(".*")
        assert len(self.engine._regex_strings) == 1
        assert len(self.engine.regular_expressions_entities) == 1

    def testSelectBestIntent(self):
        parser1 = IntentBuilder("Parser1").require("Entity1").build()
        self.engine.register_entity("tree", "Entity1")
        self.engine.register_intent_parser(parser1)

        utterance = "go to the tree house"
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        assert intent['intent_type'] == 'Parser1'

        parser2 = IntentBuilder("Parser2").require("Entity1").require("Entity2").build()
        self.engine.register_entity("house", "Entity2")
        self.engine.register_intent_parser(parser2)
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        assert intent['intent_type'] == 'Parser2'

    def testIntentMissingEntity(self):
        utterance1 = "give me One home"
        utterance2 = "give me One or Two"
        parser3 = IntentBuilder("Parser3").require("One").require("Two").build()
        self.engine.register_entity("One","One")
        self.engine.register_entity("Two","Two")
        self.engine.register_intent_parser(parser3)
        intent2 = self.engine.determine_intent(utterance2)
        #print "intent2", intent2
        try:
            intent2 = next(intent2)
            #print intent2['intent_type']
        except:
            pass
        intent1 = self.engine.determine_intent(utterance1)
        #print intent1
        try:
            intent1 = next(intent1)
            #print intent1['intent_type']
        except:
            pass
