from tools.text.tokenizer import EnglishTokenizer
from tools.text.trie import Trie

__author__ = 'seanfitz'


class EntityTagger(object):
    def __init__(self, trie, tokenizer, regex_entities=[], max_tokens=20):
        self.trie = trie
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens
        self.regex_entities = regex_entities

    def tag(self, utterance):
        tokens = self.tokenizer.tokenize(utterance)

        entities = []

        for i in xrange(len(tokens)):
            part = ' '.join(tokens[i:])
            if len(self.regex_entities) > 0:
                local_trie = Trie()
                for regex_entity in self.regex_entities:
                    match = regex_entity.search(part)
                    groups = match.groupdict() if match else {}
                    for key in groups.keys():
                        match_str = groups.get(key)
                        local_trie.insert(match_str, key)
                sub_tagger = EntityTagger(local_trie, self.tokenizer, max_tokens=self.max_tokens)
                for sub_entity in sub_tagger.tag(part):
                    sub_entity['start_token'] += i
                    sub_entity['end_token'] += i
                    entities.append(sub_entity)

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