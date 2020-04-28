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

        self.engine.register_intent_parser(intent1)
        self.engine.register_intent_parser(intent2)

        self.engine.register_entity("what time is it", "TimeQuery")
        self.engine.register_entity("seattle", "Location")
        self.engine.register_entity("miami", "Location")

        self.engine.register_entity("weather", "WeatherKeyword")

        utterance1 = "what time is it in seattle"
        intent = next(self.engine.determine_intent(utterance1, include_tags=True, context_manager=self.context_manager))
        assert intent
        assert intent['intent_type'] == 'TimeQueryIntent'
        assert '__tags__' in intent
        for tag in intent['__tags__']:
            context_entity = tag.get('entities')[0]
            self.context_manager.inject_context(context_entity)

        utterance2 = "what's the weather like?"
        intent = next(self.engine.determine_intent(utterance2, context_manager=self.context_manager))
        assert intent
        assert intent['intent_type'] == 'WeatherQueryIntent'

    def testContextOnlyUsedOnce(self):
        intent_parser = IntentBuilder("DummyIntent")\
            .require("Foo")\
            .optionally("Foo", "Foo2")\
            .build()

        context_entity = {'confidence': 1.0, 'data': [('foo', 'Foo')], 'match': 'foo', 'key': 'foo'}
        self.context_manager.inject_context(context_entity)
        self.engine.register_intent_parser(intent_parser)
        self.engine.register_entity("foo", "Foo")
        self.engine.register_entity("fop", "Foo")

        intent = next(self.engine.determine_intent("foo", include_tags=True, context_manager=self.context_manager))
        assert intent
        assert intent['intent_type'] == "DummyIntent"
        assert not (intent.get("Foo") and intent.get("Foo2"))

    def testContextAndOneOf(self):
        # test to cover https://github.com/MycroftAI/adapt/issues/86
        engine = IntentDeterminationEngine()
        context_manager = ContextManager()

        # define vocabulary
        weather_keyword = [
            "weather"
        ]

        for wk in weather_keyword:
            engine.register_entity(wk, "WeatherKeyword")

        # structure intent
        weather_intent = IntentBuilder("WeatherIntent") \
            .require("WeatherKeyword") \
            .one_of("Location", "LocationContext").build()

        engine.register_intent_parser(weather_intent)
        word = 'lizard'
        context = 'LocationContext'
        entity = {}
        entity['data'] = [(word, context)]
        entity['match'] = word
        entity['key'] = word
        context_manager.inject_context(entity)

        intents = list(engine.determine_intent('weather', context_manager=context_manager))
        self.assertEqual(1, len(intents), "Incorrect number of intents")
        result = intents[0]
        self.assertEqual("lizard", result.get("LocationContext"), "Context not matched")
        self.assertEqual(0.75, result.get('confidence'), "Context confidence not properly applied.")




