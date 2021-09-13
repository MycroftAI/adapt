import pickle

from adapt.engine import DomainIntentDeterminationEngine, \
    IntentDeterminationEngine

EXPECTED_ENGINES = set([
    IntentDeterminationEngine,
    DomainIntentDeterminationEngine,
])

SAFE_CLASSES = [
    ("adapt.engine", "IntentDeterminationEngine"),
    ("adapt.engine", "DomainIntentDeterminationEngine"),
    ("adapt.tools.text.tokenizer", "EnglishTokenizer"),
    ("adapt.tools.text.trie", "Trie"),
    ("adapt.tools.text.trie", "TrieNode"),
    ("adapt.intent", "Intent")
]


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) not in SAFE_CLASSES:
            raise pickle.UnpicklingError("Attempted illegal import: "
                                         "{}.{}".format(module, name))
        return pickle.Unpickler.find_class(self, module, name)


def load(filename):
    """
    Load a file that contains a serialized intent determination engine.
    :param filename (str): source path
    :return: An instance of IntentDeterminationEngine or
        DomainIntentDeterminationEngine
    """
    with open(filename, 'rb') as f:
        engine = RestrictedUnpickler(f).load()
        if engine.__class__ not in EXPECTED_ENGINES:
            raise ValueError("Was expecting to instantiate an "
                             "IntentDeterminationEngine, but instead found "
                             "{}".format(engine.__class__))
        return engine


def dump(engine, filename):
    """
    Serialize an adapt Intent engine and write it to the target file.
    :param engine (IntentDeterminationEngine or DomainIntentDeterminationEngine):
    :param filename (str): destination path
    """
    with open(filename, 'wb') as f:
        pickle.dump(engine, f)
