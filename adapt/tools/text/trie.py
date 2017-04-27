__author__ = 'seanfitz'


class TrieNode(object):
    def __init__(self, data=None, is_terminal=False):
        self.data = set()
        if data:
            self.data.add(data)
        self.is_terminal = is_terminal
        self.children = {}
        self.key = None
        # since weight is an attribute on the node (and not on the payload), all
        # payloads at this node have the weight of the last insert.
        self.weight = 1.0

    def lookup(self, iterable, index=0, gather=False, edit_distance=0, max_edit_distance=0, match_threshold=0.0, matched_length=0):
        """
        TODO: Implement trie lookup with edit distance

        Args:
            iterable(list?): key used to find what is requested this could
                be a generator.
            index(int): index of what is requested
            gather(bool): of weather to gather or not
            edit_distance(int): the distance -- currently not used
            max_edit_distance(int): the max distance -- not currently used

        yields:
            object: yields the results of the search
        """
        if self.is_terminal:
            if index == len(iterable) or \
                    (gather and index < len(iterable) and iterable[index] == ' '):  # only gather on word break)
                confidence = float(len(self.key) - edit_distance) / float(max(len(self.key), index))
                if confidence > match_threshold:
                    yield {
                        'key': self.key,
                        'match': iterable[:index],
                        'data': self.data,
                        'confidence': confidence * self.weight
                    }

        if index < len(iterable) and iterable[index] in self.children:
            for result in self.children[iterable[index]]\
                    .lookup(iterable, index + 1, gather=gather,
                            edit_distance=edit_distance, max_edit_distance=max_edit_distance, matched_length=matched_length + 1):
                yield result

        # if there's edit distance remaining and it's possible to match a word above the confidence threshold
        potential_confidence = float(index - edit_distance + (max_edit_distance - edit_distance)) / \
                               (float(index) + (max_edit_distance - edit_distance)) if index + max_edit_distance - edit_distance > 0 else 0.0
        if edit_distance < max_edit_distance and potential_confidence > match_threshold:
            for child in list(self.children):
                if index >= len(iterable) or child != iterable[index]:
                    # substitution
                    for result in self.children[child]\
                        .lookup(iterable, index + 1, gather=gather,
                                edit_distance=edit_distance + 1, max_edit_distance=max_edit_distance, matched_length=matched_length):
                        yield result
                    # delete
                    for result in self.children[child]\
                        .lookup(iterable, index + 2, gather=gather,
                                edit_distance=edit_distance + 1, max_edit_distance=max_edit_distance, matched_length=matched_length):
                        yield result
                    # insert
                    for result in self.children[child]\
                        .lookup(iterable, index, gather=gather,
                                edit_distance=edit_distance + 1, max_edit_distance=max_edit_distance, matched_length=matched_length):
                        yield result

    def insert(self, iterable, index=0, data=None, weight=1.0):
        """Insert new node into tree

        Args:
            iterable(hashable): key used to find in the future.
            data(object): data associated with the key
            index(int): an index used for insertion.
            weight(float): the wait given for the item added.
        """
        if index == len(iterable):
            self.is_terminal = True
            self.key = iterable
            self.weight = weight
            if data:
                self.data.add(data)
        else:
            if iterable[index] not in self.children:
                self.children[iterable[index]] = TrieNode()
            self.children[iterable[index]].insert(iterable, index + 1, data)

    def is_prefix(self, iterable, index=0):
        if iterable[index] in self.children:
            return self.children[iterable[index]].is_prefix(iterable, index + 1)
        else:
            return False

    def remove(self, iterable, data=None, index=0):
        """Remove an element from the trie

        Args
            iterable(hashable): key used to find what is to be removed
            data(object): data associated with the key
            index(int): index of what is to me removed

        Returns:
        bool:
            True: if it was removed
            False: if it was not removed
        """
        if index == len(iterable):
            if self.is_terminal:
                if data:
                    self.data.remove(data)
                    if len(self.data) == 0:
                        self.is_terminal = False
                else:
                    self.data.clear()
                    self.is_terminal = False
                return True
            else:
                return False
        elif iterable[index] in self.children:
            return self.children[iterable[index]].remove(iterable, index=index+1, data=data)
        else:
            return False


class Trie(object):
    """Interface for the tree

        Attributes:
            root(TrieNode): parent node to start the tree
            max_edit_distance(int): ?
            match_threshold(int): ?

    """

    def __init__(self, max_edit_distance=0, match_threshold=0.0):
        """Init the Trie object and create root node.

        Creates an Trie object with a root node with the passed in
        max_edit_distance and match_threshold.

        Args:
            max_edit_distance(int): ?
            match_threshold(int): ?

        Notes:
            This never seems to get called with max_edit_distance or match_threshold
        """
        self.root = TrieNode('root')
        self.max_edit_distance = max_edit_distance
        self.match_threshold = match_threshold

    def gather(self, iterable):
        """Calls the lookup with gather True Passing iterable and yields
        the result.
        """
        for result in self.lookup(iterable, gather=True):
            yield result

    def lookup(self, iterable, gather=False):
        """Call the lookup on the root node with the given parameters.

        Args
            iterable(index or key): Used to retrive nodes from tree
            gather(bool): this is passed down to the root node lookup

        Notes:
            max_edit_distance and match_threshold come from the init
        """
        for result in self.root.lookup(iterable,
                                       gather=gather,
                                       edit_distance=0,
                                       max_edit_distance=self.max_edit_distance,
                                       match_threshold=self.match_threshold):
            yield result

    def insert(self, iterable, data=None, weight=1.0):
        """Used to insert into he root node

        Args
            iterable(hashable): index or key used to identify
            data(object): data to be paired with the key
        """
        self.root.insert(iterable, index=0, data=data, weight=1.0)

    def remove(self, iterable, data=None):
        """Used to remove from the root node

        Args:
            iterable(hashable): index or key used to identify
                item to remove
            data: data to be paired with the key
        """
        return self.root.remove(iterable, data=data)
