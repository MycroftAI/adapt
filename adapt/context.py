from six.moves import xrange

__author__ = "seanfitz"


class ContextManagerFrame(object):
    """
    Manages entities and context for a single frame of conversation.
    Provides simple equality querying.
    """
    def __init__(self, entities=[], metadata={}):
        self.entities = entities
        self.metadata = metadata

    def metadata_matches(self, query={}):
        result = len(query.keys()) > 0
        for key in query.keys():
            result = result and query[key] == self.metadata.get(key)

        return result

    def merge_context(self, tag, metadata):
        self.entities.append(tag)
        for k in metadata.keys():
            if k not in self.metadata:
                self.metadata[k] = k


class ContextManager(object):
    """
    ContextManager
    Use to track context throughout the course of a conversational session. How to manage a session's
    lifecycle is not captured here.
    """
    def __init__(self):
        self.frame_stack = []

    def inject_context(self, entity, metadata={}):
        """
        :param entity:
            format {'data': 'Entity tag as <str>', 'key': 'entity proper name as <str>', 'confidence': <float>'}

        :param metadata: dict, arbitrary metadata about the entity being added

        :return:
        """
        top_frame = self.frame_stack[0] if len(self.frame_stack) > 0 else None
        if top_frame and top_frame.metadata_matches(metadata):
            top_frame.merge_context(entity, metadata)
        else:
            frame = ContextManagerFrame(entities=[entity], metadata=metadata.copy())
            self.frame_stack.insert(0, frame)

    def get_context(self, max_frames=None, missing_entities=[]):
        """
        Constructs a list of entities from the context.

        :param max_frames: integer, max number of frames to look back

        :param missing_entities: a list or set of tag names, as strings

        :return: a list of entities
        """
        if not max_frames:
            max_frames = len(self.frame_stack)

        missing_entities = list(missing_entities)
        context = []
        for i in xrange(max_frames):
            frame_entities = [entity.copy() for entity in self.frame_stack[i].entities]
            for entity in frame_entities:
                entity['confidence'] = entity.get('confidence', 1.0) / (2.0 + i)
            context += frame_entities

        result = []
        if len(missing_entities) > 0:
            for entity in context:
                if entity.get('data') in missing_entities:
                    result.append(entity)
                    # NOTE: this implies that we will only ever get one
                    # of an entity kind from context, unless specified
                    # multiple times in missing_entities. Cannot get
                    # an arbitrary number of an entity kind.
                    missing_entities.remove(entity.get('data'))
        else:
            result = context

        return result



