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
        self.engine.register_intent_parser(parser1)
        self.engine.register_entity("tree", "Entity1")

        utterance = "go to the tree house"
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        assert intent['intent_type'] == 'Parser1'

        parser2 = IntentBuilder("Parser2").require("Entity1").require("Entity2").build()
        self.engine.register_intent_parser(parser2)
        self.engine.register_entity("house", "Entity2")
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        assert intent['intent_type'] == 'Parser2'

    def testDropIntent(self):
        parser1 = IntentBuilder("Parser1").require("Entity1").build()
        self.engine.register_intent_parser(parser1)
        self.engine.register_entity("tree", "Entity1")

        parser2 = (IntentBuilder("Parser2").require("Entity1")
                   .require("Entity2").build())
        self.engine.register_intent_parser(parser2)
        self.engine.register_entity("house", "Entity2")

        utterance = "go to the tree house"

        intent = next(self.engine.determine_intent(utterance))
        assert intent
        assert intent['intent_type'] == 'Parser2'

        assert self.engine.drop_intent_parser('Parser2') is True
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        assert intent['intent_type'] == 'Parser1'

    def testDropEntity(self):
        parser1 = IntentBuilder("Parser1").require("Entity1").build()
        self.engine.register_intent_parser(parser1)
        self.engine.register_entity("laboratory", "Entity1")
        self.engine.register_entity("lab", "Entity1")

        utterance = "get out of my lab"
        utterance2 = "get out of my laboratory"
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        assert intent['intent_type'] == 'Parser1'

        intent = next(self.engine.determine_intent(utterance2))
        assert intent
        assert intent['intent_type'] == 'Parser1'

        # Remove Entity and re-register laboratory and make sure only that
        # matches.
        self.engine.drop_entity(entity_type='Entity1')
        self.engine.register_entity("laboratory", "Entity1")

        # Sentence containing lab should not produce any results
        with self.assertRaises(StopIteration):
            intent = next(self.engine.determine_intent(utterance))

        # But sentence with laboratory should
        intent = next(self.engine.determine_intent(utterance2))
        assert intent
        assert intent['intent_type'] == 'Parser1'

    def testCustomDropEntity(self):
        parser1 = (IntentBuilder("Parser1").one_of("Entity1", "Entity2")
                   .build())
        self.engine.register_intent_parser(parser1)
        self.engine.register_entity("laboratory", "Entity1")
        self.engine.register_entity("lab", "Entity2")

        utterance = "get out of my lab"
        utterance2 = "get out of my laboratory"
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        assert intent['intent_type'] == 'Parser1'

        intent = next(self.engine.determine_intent(utterance2))
        assert intent
        assert intent['intent_type'] == 'Parser1'

        def matcher(data):
            return data[1].startswith('Entity')

        self.engine.drop_entity(match_func=matcher)
        self.engine.register_entity("laboratory", "Entity1")

        # Sentence containing lab should not produce any results
        with self.assertRaises(StopIteration):
            intent = next(self.engine.determine_intent(utterance))

        # But sentence with laboratory should
        intent = next(self.engine.determine_intent(utterance2))
        assert intent

    def testDropRegexEntity(self):
        self.engine.register_regex_entity(r"the dog (?P<Dog>.*)")
        self.engine.register_regex_entity(r"the cat (?P<Cat>.*)")
        assert len(self.engine._regex_strings) == 2
        assert len(self.engine.regular_expressions_entities) == 2
        self.engine.drop_regex_entity(entity_type='Cat')
        assert len(self.engine._regex_strings) == 1
        assert len(self.engine.regular_expressions_entities) == 1

    def testCustomDropRegexEntity(self):
        self.engine.register_regex_entity(r"the dog (?P<SkillADog>.*)")
        self.engine.register_regex_entity(r"the cat (?P<SkillACat>.*)")
        self.engine.register_regex_entity(r"the mangy dog (?P<SkillBDog>.*)")
        assert len(self.engine._regex_strings) == 3
        assert len(self.engine.regular_expressions_entities) == 3

        def matcher(regexp):
            """Matcher for all match groups defined for SkillB"""
            match_groups = regexp.groupindex.keys()
            return any([k.startswith('SkillB') for k in match_groups])

        self.engine.drop_regex_entity(match_func=matcher)
        assert len(self.engine._regex_strings) == 2
        assert len(self.engine.regular_expressions_entities) == 2

    def testAddingOfRemovedRegexp(self):
        self.engine.register_regex_entity(r"the cool (?P<thing>.*)")

        def matcher(regexp):
            """Matcher for all match groups defined for SkillB"""
            match_groups = regexp.groupindex.keys()
            return any([k.startswith('thing') for k in match_groups])

        self.engine.drop_regex_entity(match_func=matcher)
        assert len(self.engine.regular_expressions_entities) == 0
        self.engine.register_regex_entity(r"the cool (?P<thing>.*)")
        assert len(self.engine.regular_expressions_entities) == 1

    def testUsingOfRemovedRegexp(self):
        self.engine.register_regex_entity(r"the cool (?P<thing>.*)")
        parser = IntentBuilder("Intent").require("thing").build()
        self.engine.register_intent_parser(parser)

        def matcher(regexp):
            """Matcher for all match groups defined for SkillB"""
            match_groups = regexp.groupindex.keys()
            return any([k.startswith('thing') for k in match_groups])

        self.engine.drop_regex_entity(match_func=matcher)
        assert len(self.engine.regular_expressions_entities) == 0

        utterance = "the cool cat"
        intents = [match for match in self.engine.determine_intent(utterance)]
        assert len(intents) == 0

    def testEmptyTags(self):
        # Validates https://github.com/MycroftAI/adapt/issues/114
        engine = IntentDeterminationEngine()
        engine.register_entity("Kevin",
                               "who")  # same problem if several entities
        builder = IntentBuilder("Buddies")
        builder.optionally("who")  # same problem if several entity types
        engine.register_intent_parser(builder.build())

        intents = [i for i in engine.determine_intent("Julien is a friend")]
        assert len(intents) == 0

    def testResultsAreSortedByConfidence(self):
        self.engine.register_entity('what is', 'Query', None)
        self.engine.register_entity('weather', 'Weather', None)
        self.engine.register_regex_entity('(at|in) (?P<Location>.+)')
        self.engine.register_regex_entity('(?P<Entity>.*)')

        i = IntentBuilder("CurrentWeatherIntent").require(
            "Weather").optionally("Location").build()
        self.engine.register_intent_parser(i)
        utterance = "what is the weather like in stockholm"
        intents = [
            i for i in self.engine.determine_intent(utterance, num_results=100)
        ]
        confidences = [intent.get('confidence', 0.0) for intent in intents]
        assert len(confidences) > 1
        assert all(confidences[i] >= confidences[i+1] for i in range(len(confidences)-1))

    def testExclude(self):
        parser1 = IntentBuilder("Parser1").require("Entity1").exclude("Entity2").build()
        self.engine.register_intent_parser(parser1)

        parser2 = IntentBuilder("Parser2").require("Entity1").exclude("Entity3").build()
        self.engine.register_intent_parser(parser2)

        self.engine.register_entity("go", "Entity1")
        self.engine.register_entity("tree", "Entity2")
        self.engine.register_entity("house", "Entity3")

        # Parser 1 cannot contain the word tree
        utterance = "go to the tree"
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        assert intent['intent_type'] == 'Parser2'

        # Parser 2 cannot contain the word house
        utterance = "go to the house"
        intent = next(self.engine.determine_intent(utterance))
        assert intent
        assert intent['intent_type'] == 'Parser1'

        # Should fail because both excluded words are present
        utterance = "go to the tree house"
        with self.assertRaises(StopIteration):
            intent = next(self.engine.determine_intent(utterance))
