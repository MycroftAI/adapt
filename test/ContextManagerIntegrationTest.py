from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder

__author__ = "seanfitz"

import unittest


class ContextManagerIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.engine = IntentDeterminationEngine()

    def testBasicContextualFollowup(self):
        intent1 = IntentBuilder("TimeQueryIntent")\
            .require("TimeQuery")\
            .require("Location")\
            .build()
        intent2 = IntentBuilder("WeatherQueryIntent")\
            .require("WeatherKeyword")\
            .require("Location")\
            .build()

        self.engine.register_intent_parser(intent1)
        self.engine.register_intent_parser(intent2)

        self.engine.register_entity("what time is it", "TimeQuery")
        self.engine.register_entity("seattle", "Location")
        self.engine.register_entity("miami", "Location")

        self.engine.register_entity("weather", "WeatherKeyword")

        utterance1 = "what time is it in seattle"
        intent = next(self.engine.determine_intent(utterance1))
        assert intent
        assert intent['intent_type'] == 'TimeQueryIntent'

        utterance2 = "what's the weather like?"
        intent = next(self.engine.determine_intent(utterance2))
        assert intent
        assert intent['intent_type'] == 'WeatherQueryIntent'
