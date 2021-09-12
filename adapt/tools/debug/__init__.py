import pickle

from adapt.engine import DomainIntentDeterminationEngine, \
    IntentDeterminationEngine

EXPECTED_ENGINES = set([
    IntentDeterminationEngine,
    DomainIntentDeterminationEngine,
])


def load(filename):
    """
    Load a file that contains a serialized intent determination engine.
    :param filename (str): source path
    :return: An instance of IntentDeterminationEngine or
        DomainIntentDeterminationEngine
    """
    with open(filename, 'rb') as f:
        engine = pickle.load(f)
        if engine.__class__ not in EXPECTED_ENGINES:
            raise ValueError(f"Was expecting to instantiate an "
                             f"IntentDeterminationEngine, but instead found "
                             f"{engine.__class__}")
        return engine


def dump(engine, filename):
    """
    Serialize an adapt Intent engine and write it to the target file.
    :param engine (IntentDeterminationEngine or DomainIntentDeterminationEngine):
    :param filename (str): destination path
    """
    with open(filename, 'wb') as f:
        pickle.dump(engine, f)
