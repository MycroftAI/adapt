import unittest

from adapt.context import ContextManager


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
        assert context[1].get('confidence') == 1.0/3.0
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

