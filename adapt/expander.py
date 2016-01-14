from six.moves import xrange

__author__ = 'seanfitz'


class SimpleGraph(object):
    def __init__(self):
        self.adjacency_lists = {}

    def add_edge(self, a, b):
        neighbors_of_a = self.adjacency_lists.get(a)
        if not neighbors_of_a:
            neighbors_of_a = set()
            self.adjacency_lists[a] = neighbors_of_a

        neighbors_of_a.add(b)

        neighbors_of_b = self.adjacency_lists.get(b)
        if not neighbors_of_b:
            neighbors_of_b = set()
            self.adjacency_lists[b] = neighbors_of_b

        neighbors_of_b.add(a)

    def get_neighbors_of(self, a):
        return self.adjacency_lists.get(a, set())

    def vertex_set(self):
        return list(self.adjacency_lists)


def bronk(r, p, x, graph):
    if len(p) == 0 and len(x) == 0:
        yield r
        return
    for vertex in p[:]:
        r_new = r[::]
        r_new.append(vertex)
        p_new = [val for val in p if val in graph.get_neighbors_of(vertex)] # p intersects N(vertex)
        x_new = [val for val in x if val in graph.get_neighbors_of(vertex)] # x intersects N(vertex)
        for result in bronk(r_new, p_new, x_new, graph):
            yield result
        p.remove(vertex)
        x.append(vertex)


def get_cliques(vertices, graph):
    for clique in bronk([], vertices, [], graph):
        yield clique


def graph_key_from_tag(tag, entity_index):
    start_token = tag.get('start_token')
    entity = tag.get('entities', [])[entity_index]
    return str(start_token) + '-' + entity.get('key') + '-' + str(entity.get('confidence'))


class Lattice(object):
    def __init__(self):
        self.nodes = []

    def append(self, data):
        if isinstance(data, list) and len(data) > 0:
            self.nodes.append(data)
        else:
            self.nodes.append([data])

    def traverse(self, index=0):
        if index < len(self.nodes):
            for entity in self.nodes[index]:
                for next_result in self.traverse(index=index+1):
                    if isinstance(entity, list):
                        yield entity + next_result
                    else:
                        yield [entity] + next_result
        else:
            yield []


class BronKerboschExpander(object):
    """
    BronKerboschExpander

    Given a list of tagged entities (from the existing entity tagger implementation or another), expand out
    valid parse results.

    A parse result is considered valid if it contains no overlapping spans.

    Since total confidence of a parse result is based on the sum of confidences of the entities, there is no sense
    in yielding any potential parse results that are a subset/sequence of a larger valid parse result. By comparing
    this concept to that of maximal cliques (https://en.wikipedia.org/wiki/Clique_problem), we can use well known
    solutions to the maximal clique problem like the Bron/Kerbosch algorithm (https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm).

    By considering tagged entities that do not overlap to be "neighbors", BronKerbosch will yield a set of maximal
    cliques that are also valid parse results.
    """
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def _build_graph(self, tags):
        graph = SimpleGraph()
        for tag_index in xrange(len(tags)):
            for entity_index in xrange(len(tags[tag_index].get('entities'))):
                a_entity_name = graph_key_from_tag(tags[tag_index], entity_index)
                tokens = self.tokenizer.tokenize(tags[tag_index].get('entities', [])[entity_index].get('match'))
                for tag in tags[tag_index + 1:]:
                    start_token = tag.get('start_token')
                    if start_token >= tags[tag_index].get('start_token') + len(tokens):
                        for b_entity_index in xrange(len(tag.get('entities'))):
                            b_entity_name = graph_key_from_tag(tag, b_entity_index)
                            graph.add_edge(a_entity_name, b_entity_name)

        return graph

    def _sub_expand(self, tags):
        entities = {}
        graph = self._build_graph(tags)

        # name entities
        for tag in tags:
            for entity_index in xrange(len(tag.get('entities'))):
                node_name = graph_key_from_tag(tag, entity_index)
                if not node_name in entities:
                    entities[node_name] = []
                entities[node_name] += [
                    tag.get('entities', [])[entity_index],
                    tag.get('entities', [])[entity_index].get('confidence'),
                    tag
                ]

        for clique in get_cliques(list(entities), graph):
            result = []
            for entity_name in clique:
                start_token = int(entity_name.split("-")[0])
                old_tag = entities[entity_name][2]
                tag = {
                    'start_token': start_token,
                    'entities': [entities.get(entity_name)[0]],
                    'confidence': entities.get(entity_name)[1] * old_tag.get('confidence', 1.0),
                    'end_token': old_tag.get('end_token'),
                    'match': old_tag.get('entities')[0].get('match'),
                    'key': old_tag.get('entities')[0].get('key')
                }
                result.append(tag)
            result = sorted(result, key=lambda e: e.get('start_token'))
            yield result

    def expand(self, tags, clique_scoring_func=None):
        lattice = Lattice()
        overlapping_spans = []

        def end_token_index():
            return max([t.get('end_token') for t in overlapping_spans])

        for i in xrange(len(tags)):
            tag = tags[i]

            if len(overlapping_spans) > 0 and end_token_index() >= tag.get('start_token'):
                overlapping_spans.append(tag)
            elif len(overlapping_spans) > 1:
                cliques = list(self._sub_expand(overlapping_spans))
                if clique_scoring_func:
                    cliques = sorted(cliques, key=lambda e: -1 * clique_scoring_func(e))
                lattice.append(cliques)
                overlapping_spans = [tag]
            else:
                lattice.append(overlapping_spans)
                overlapping_spans = [tag]
        if len(overlapping_spans) > 1:
            cliques = list(self._sub_expand(overlapping_spans))
            if clique_scoring_func:
                    cliques = sorted(cliques, key=lambda e: -1 * clique_scoring_func(e))
            lattice.append(cliques)
        else:
            lattice.append(overlapping_spans)

        return lattice.traverse()

