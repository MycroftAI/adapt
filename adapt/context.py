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

"""
Context Management code for Adapt (where context ~= persistent session state).
"""
from six.moves import xrange

__author__ = "seanfitz, Art McGee"


class ContextManagerFrame(object):
    """
    Manages entities and context for a single frame of conversation.
    Provides simple equality querying.

    Attributes:
        entities(list): Entities that belong to ContextManagerFrame
        metadata(object): metadata to describe context belonging to ContextManagerFrame
    """
    def __init__(self, entities=None, metadata=None):
        """
        Initialize ContextManagerFrame

        Args:
            entities(list): List of Entities...
            metadata(object): metadata to describe context?
        """
        self.entities = entities or []
        self.metadata = metadata or {}

    def metadata_matches(self, query=None):
        """
        Returns key matches to metadata

        Asserts that the contents of query exist within (logical subset of)
        metadata in this frame.
        Args:
            query(object): metadata for matching

        Returns:
            bool:
                True: when key count in query is > 0 and all keys in query in
                    self.metadata
                False: if key count in query is <= 0 or any key in query not
                    found in self.metadata

        """
        query = query or {}
        result = len(query.keys()) > 0
        for key in query.keys():
            result = result and query[key] == self.metadata.get(key)

        return result

    def merge_context(self, tag, metadata):
        """
        merge into contextManagerFrame new entity and metadata.

        Appends tag as new entity and adds keys in metadata to keys in
        self.metadata.

        Args:
            tag(str): entity to be added to self.entities
            metadata(object): metadata containes keys to be added to self.metadata
        """
        self.entities.append(tag)
        for k, v in metadata.items():
            if k not in self.metadata:
                self.metadata[k] = v


class ContextManager(object):
    """
    ContextManager
    Use to track context throughout the course of a conversational session.
    How to manage a session's lifecycle is not captured here.
    """
    def __init__(self):
        self.frame_stack = []

    def inject_context(self, entity, metadata=None):
        """
        Add an entity to the current context.
        If metadata matches the top of the context frame stack, merge.
        Else, create a new frame and push it on top of the stack.
        Args:
            entity(object):
                format {'data': 'Entity tag as <str>',
                        'key': 'entity proper name as <str>',
                         'confidence': <float>'
                         }
            metadata(object): dict, arbitrary metadata about the entity being added
        """
        metadata = metadata or {}
        top_frame = self.frame_stack[0] if len(self.frame_stack) > 0 else None
        if top_frame and top_frame.metadata_matches(metadata):
            top_frame.merge_context(entity, metadata)
        else:
            frame = ContextManagerFrame(entities=[entity], metadata=metadata.copy())
            self.frame_stack.insert(0, frame)

    def get_context(self, max_frames=None, missing_entities=None):
        """
        Returns context, including decaying weights based on depth in stack.

        Args:
            max_frames(int): maximum number of frames to look back
            missing_entities(list of str): a list or set of tag names, as strings

        Returns:
            list: a list of entities
        """
        missing_entities = missing_entities or []
        if not max_frames or max_frames > len(self.frame_stack):
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



