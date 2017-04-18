from adapt.context import ContextManager
from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder

__author__ = "seanfitz"

import unittest


class ContextManagerIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.context_manager = ContextManager()
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

        self.engine.register_entity("what time is it", "TimeQuery")
        self.engine.register_entity("seattle", "Location")
        self.engine.register_entity("miami", "Location")

        self.engine.register_entity("weather", "WeatherKeyword")

        self.engine.register_intent_parser(intent1)
        self.engine.register_intent_parser(intent2)

        utterance1 = "what time is it in seattle"
        intent = next(
            self.engine.determine_intent(
                utterance1,
                include_tags=True,
                context_manager=self.context_manager))
        assert intent
        assert intent['intent_type'] == 'TimeQueryIntent'
        assert '__tags__' in intent
        for tag in intent['__tags__']:
            context_entity = tag.get('entities')[0]
            self.context_manager.inject_context(context_entity)

        utterance2 = "what's the weather like?"
        intent = next(
            self.engine.determine_intent(
                utterance2,
                context_manager=self.context_manager))
        assert intent
        assert intent['intent_type'] == 'WeatherQueryIntent'

    def testContextOnlyUsedOnce(self):
        intent_parser = IntentBuilder("DummyIntent")\
            .require("Foo")\
            .optionally("Foo", "Foo2")\
            .build()

        context_entity = {'confidence': 1.0, 'data': [
            ('foo', 'Foo')], 'match': 'foo', 'key': 'foo'}
        self.context_manager.inject_context(context_entity)
        self.engine.register_entity("foo", "Foo")
        self.engine.register_entity("fop", "Foo")
        self.engine.register_intent_parser(intent_parser)

        intent = next(
            self.engine.determine_intent(
                "foo",
                include_tags=True,
                context_manager=self.context_manager))
        assert intent
        assert intent['intent_type'] == "DummyIntent"
        assert not (intent.get("Foo") and intent.get("Foo2"))
