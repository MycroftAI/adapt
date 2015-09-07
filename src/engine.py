__author__ = 'seanfitz'


class Entity(object):
    def __init__(self, entity_type, entity_value):
        self.entity_type = entity_type
        self.entity_value = entity_value


class Transformer(object):
    def __init__(self, required_input_types=[], optional_input_types=[], output_types=[]):
        self.required_input_types = required_input_types
        self.optional_input_types = optional_input_types
        self.output_types = output_types

    def transform(self, inputs):
        raise Exception("Not Implemented")

    def is_input(self, input_type):
        return input_type in self.required_input_types + self.optional_input_types

    def validate_input(self, inputs):
        input_types = [i.entity_type for i in inputs]

        for required_input in self.required_input_types:
            if required_input in input_types:
                input_types.remove(required_input)
            else:
                return False

        return True




class Engine(object):
    def __init__(self, transformers):
        self.transformers = transformers

    def solve(self, entities):
        pass

    def breakdown_entities(self, entities):
        result = []
        for entity in entities:

            for k in entity.__dict__:
                if k == 'entity_type':
                    continue
                elif k == 'entity_value':
                    result.append(entity.__dict__[k])
                else:
                    result.append(Entity(k, entity.__dict__[k]))

        return result