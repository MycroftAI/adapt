from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie

__author__ = 'seanfitz'


class EntityTagger(object):
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

    def tag(self, utterance):
        tokens = self.tokenizer.tokenize(utterance)
        entities = []
        if len(self.regex_entities) > 0:
            for part, idx in self._iterate_subsequences(tokens):
                local_trie = Trie()
                for regex_entity in self.regex_entities:
                    match = regex_entity.match(part)
                    groups = match.groupdict() if match else {}
                    for key in groups.keys():
                        match_str = groups.get(key)
                        local_trie.insert(match_str, key)
                sub_tagger = EntityTagger(local_trie, self.tokenizer, max_tokens=self.max_tokens)
                for sub_entity in sub_tagger.tag(part):
                    sub_entity['start_token'] += idx
                    sub_entity['end_token'] += idx
                    for e in sub_entity['entities']:
                        e['confidence'] = 0.5
                    entities.append(sub_entity)

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

        return entities


if __name__ == "__main__":
    tokenizer = EnglishTokenizer()
    trie = Trie()
    mypath = '/media/seanfitz/DATA01/facts'
    from os import listdir
    from os.path import isfile, join
    import json

    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

    for f in onlyfiles:
        print("Loading facts from %s..." % f)
        fact_file = open(f)
        for line in fact_file.readlines():
            fact = json.loads(line)
            trie.insert(fact.get('start'))
            trie.insert(fact.get('end'))

    tagger = EntityTagger(trie, tokenizer)
    tags = tagger.tag("play season one of falling skies")
    for tag in tags:
        print tag