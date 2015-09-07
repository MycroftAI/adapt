__author__ = 'seanfitz'

HUB_CLIENT_ENTITY_NAME = 'Hub Client'

def is_entity(tag, entity_name):
    for entity in tag.get('entities'):
        for t in entity.get('data'):
            if t.lower() == entity_name.lower():
                return True
    return False


def find_first_tag(tags, entity_type, after_index=-1):
    for tag in tags:
        for entity in tag.get('entities'):
            for t in entity.get('data'):
                if t.lower() == entity_type.lower() and tag.get('start_token') > after_index:
                    return tag

    return None


def find_next_tag(tags, end_index=0):
    for tag in tags:
        if tag.get('start_token') > end_index:
            return tag
    return None


def choose_1_from_each(lists):
    if len(lists) == 0:
        yield []
    else:
        for el in lists[0]:
            for next_list in choose_1_from_each(lists[1:]):
                yield [el] + next_list


def resolve_one_of(tags, at_least_one):
    if len(tags) < len(at_least_one):
        return None
    for possible_resolution in choose_1_from_each(at_least_one):
        resolution = {}
        pr = possible_resolution[:]
        for entity_type in pr:
            last_end_index = 0
            if entity_type in resolution:
                last_end_index = resolution.get[entity_type][-1].get('end_token')
            tag = find_first_tag(tags, entity_type, after_index=last_end_index)
            if not tag:
                break
            else:
                if entity_type not in resolution:
                    resolution[entity_type] = []
                resolution[entity_type].append(tag)
        if len(resolution) == len(possible_resolution):
            return resolution

    return None


class Intent(object):
    def __init__(self, name, requires, at_least_one, optional):
        self.name = name
        self.requires = requires
        self.at_least_one = at_least_one
        self.optional = optional

    def validate(self, tags, confidence):
        result = {'intent_type': self.name}
        intent_confidence = 0.0
        local_tags = tags[:]
        for require_type, attribute_name in self.requires:
            required_tag = find_first_tag(local_tags, require_type)
            if not required_tag:
                result['confidence'] = 0.0
                return result
            result[attribute_name] = required_tag.get('key')
            local_tags.remove(required_tag)
            # TODO: use confidence based on edit distance and context
            intent_confidence += 1.0

        if len(self.at_least_one) > 0:
            best_resolution = resolve_one_of(tags, self.at_least_one)
            if not best_resolution:
                result['confidence'] = 0.0
                return result
            else:
                for key in best_resolution:
                    result[key] = best_resolution[key][0].get('key')

        for optional_type, attribute_name in self.optional:
            optional_tag = find_first_tag(local_tags, optional_type)
            if not optional_tag or attribute_name in result:
                continue
            result[attribute_name] = optional_tag.get('key')
            local_tags.remove(optional_tag)
            intent_confidence += 1.0

        total_confidence = intent_confidence / len(tags) * confidence

        target_client = find_first_tag(local_tags, HUB_CLIENT_ENTITY_NAME)

        result['target'] = target_client.get('key') if target_client else None
        result['confidence'] = total_confidence

        return result


class IntentBuilder(object):
    def __init__(self, intent_name):
        self.at_least_one = []
        self.requires = []
        self.optional = []
        self.name = intent_name

    def one_of(self, *args):
        self.at_least_one.append(args)
        return self

    def require(self, entity_type, attribute_name=None):
        if not attribute_name:
            attribute_name = entity_type
        self.requires += [(entity_type, attribute_name)]
        return self

    def optionally(self, entity_type, attribute_name=None):
        if not attribute_name:
            attribute_name = entity_type
        self.optional += [(entity_type, attribute_name)]
        return self

    def build(self):
        return  Intent(self.name, self.requires, self.at_least_one, self.optional)