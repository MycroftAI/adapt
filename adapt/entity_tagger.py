from adapt.tools.text.trie import Trie
from six.moves import xrange

__author__ = 'seanfitz'


class EntityTagger(object):
    """
    Known Entity Tagger
    Given an index of known entities, can efficiently search for those entities within a provided utterance.
    """
    def __init__(self, trie, tokenizer, regex_entities=[], max_tokens=20):
        self.trie = trie
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens
        self.regex_entities = regex_entities

    def _iterate_subsequences(self, tokens):
        """
        Using regex invokes this function, which significantly impacts performance of adapt. it is an N! operation.

        :param tokens:

        :return:
        """
        for start_idx in xrange(len(tokens)):
            for end_idx in xrange(start_idx + 1, len(tokens) + 1):
                yield ' '.join(tokens[start_idx:end_idx]), start_idx

    def _sort_and_merge_tags(self, tags):
        decorated = [(tag['start_token'], tag['end_token'], tag) for tag in tags]
        decorated.sort(key=lambda x: (x[0], x[1]))
        return [tag for start_token, end_token, tag in decorated]

    def tag(self, utterance):
        """
        Tag known entities within the utterance.

        :param utterance: a string of natural language text

        :return: dictionary, with the following keys

        match: str - the proper entity matched

        key: str - the string that was matched to the entity

        start_token: int - 0-based index of the first token matched

        end_token: int - 0-based index of the last token matched

        entities: list - a list of entity kinds as strings (Ex: Artist, Location)
        """
        tokens = self.tokenizer.tokenize(utterance)
        entities = []
        if len(self.regex_entities) > 0:
            for part, idx in self._iterate_subsequences(tokens):
                local_trie = Trie()
                for regex_entity in self.regex_entities:
                    match = regex_entity.match(part)
                    groups = match.groupdict() if match else {}
                    for key in list(groups):
                        match_str = groups.get(key)
                        local_trie.insert(match_str, (match_str, key))
                sub_tagger = EntityTagger(local_trie, self.tokenizer, max_tokens=self.max_tokens)
                for sub_entity in sub_tagger.tag(part):
                    sub_entity['start_token'] += idx
                    sub_entity['end_token'] += idx
                    for e in sub_entity['entities']:
                        e['confidence'] = 0.5
                    entities.append(sub_entity)
        additional_sort = len(entities) > 0

        for i in xrange(len(tokens)):
            part = ' '.join(tokens[i:])

            for new_entity in self.trie.gather(part):
                new_entity['data'] = list(new_entity['data'])
                entities.append({
                    'match': new_entity.get('match'),
                    'key': new_entity.get('key'),
                    'start_token': i,
                    'entities': [new_entity],
                    'end_token': i + len(self.tokenizer.tokenize(new_entity.get('match'))) - 1
                })

        if additional_sort:
            entities = self._sort_and_merge_tags(entities)

        return entities
