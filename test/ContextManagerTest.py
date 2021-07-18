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

from adapt.context import ContextManager, ContextManagerFrame


class ContextManagerFrameTest(unittest.TestCase):
    def setUp(self):
        pass

    def testMetadataMatches(self):
        frame1 = ContextManagerFrame(entities=['foo'],
                                     metadata={'domain': 'music',
                                               'foo': 'test'})

        self.assertTrue(frame1.metadata_matches({'domain': 'music'}),
                        "Should match subset of metadata")

        self.assertFalse(frame1.metadata_matches({'domain': 'weather'}),
                         "Should not match metadata value mismatch")
        self.assertTrue(
            frame1.metadata_matches({'domain': 'music', 'foo': 'test'}),
            "Should match exact metadata")
        self.assertFalse(frame1.metadata_matches(
            {'domain': 'music', 'foo': 'test', 'bar': 'test'}),
            "Should not match superset of metadata")

    def testMergeContext(self):
        frame1 = ContextManagerFrame(entities=['foo'],
                                     metadata={'domain': 'music',
                                               'foo': 'test'})

        self.assertFalse(frame1.metadata_matches({'bar': 'test'}),
                         "Should not match before merging context")

        frame1.merge_context('bar', {'domain': 'music', 'bar': 'test'})
        self.assertTrue(frame1.metadata_matches({'domain': 'music'}),
                        "Should continue to match subset of metadata")
        self.assertTrue(frame1.metadata_matches({'bar': 'test'}),
                        "Should match after merging context")


class ContextManagerTest(unittest.TestCase):
    def setUp(self):
        pass

    def testInjectRetrieveContext(self):
        manager = ContextManager()
        entity = {'key': 'Grapes of Wrath', 'data': 'Book', 'confidence': 1.0}
        manager.inject_context(entity)
        context = manager.get_context()
        assert len(context) == 1
        assert context[0].get('confidence') == 0.5

    def testInjectRetrieveContextMaxFrames(self):
        manager = ContextManager()
        entity = {'key': 'The hitchhikers guide to the galaxy',
                  'data': 'Book', 'confidence': 1.0}
        manager.inject_context(entity)
        context = manager.get_context(max_frames=2)
        assert len(context) == 1
        assert context[0].get('confidence') == 0.5

    def testNewContextNoMetadataResultsInNewFrame(self):
        manager = ContextManager()
        entity1 = {'key': 'Grapes of Wrath', 'data': 'Book', 'confidence': 1.0}
        manager.inject_context(entity1)
        context = manager.get_context()
        assert len(context) == 1
        assert context[0].get('confidence') == 0.5

        entity2 = {'key': 'Wrath of Khan', 'data': 'Film', 'confidence': 1.0}
        manager.inject_context(entity2)
        assert len(manager.frame_stack) == 2
        context = manager.get_context()
        assert len(context) == 2
        assert context[0].get('confidence') == 0.5
        assert context[0].get('data') == 'Film'
        assert context[1].get('confidence') == 1.0 / 3.0
        assert context[1].get('data') == 'Book'

    def testNewContextWithMetadataSameFrame(self):
        manager = ContextManager()
        entity1 = {'key': 'Grapes of Wrath', 'data': 'Book', 'confidence': 1.0}
        manager.inject_context(entity1, {'domain': 'media'})
        context = manager.get_context()
        assert len(context) == 1
        assert context[0].get('confidence') == 0.5

        entity2 = {'key': 'Wrath of Khan', 'data': 'Film', 'confidence': 1.0}
        manager.inject_context(entity2, {'domain': 'media'})
        assert len(manager.frame_stack) == 1
        context = manager.get_context()
        assert len(context) == 2
        assert context[0].get('confidence') == 0.5
        assert context[0].get('data') == 'Book'
        assert context[1].get('confidence') == 0.5
        assert context[1].get('data') == 'Film'
