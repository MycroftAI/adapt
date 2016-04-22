__author__ = 'the-kid89'
"""
A sample program that uses multiple intents and disambiguates by
intent confidence
try with the following:
PYTHONPATH=. python examples/multi_intent_parser.py "what's the weather like in tokyo"
PYTHONPATH=. python examples/multi_intent_parser.py "play some music by the clash"
"""

import json
import sys
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import DomainIntentDeterminationEngine


tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

engine = DomainIntentDeterminationEngine()

engine.register_domain('Domain1')
engine.register_domain('Domain2')

# define vocabulary
weather_keyword = [
    "weather"
]

for wk in weather_keyword:
    engine.register_entity(wk, "WeatherKeyword", domain='Domain1')

weather_types = [
    "snow",
    "rain",
    "wind",
    "sleet",
    "sun"
]

for wt in weather_types:
    engine.register_entity(wt, "WeatherType", domain='Domain1')

locations = [
    "Seattle",
    "San Francisco",
    "Tokyo"
]

for l in locations:
    engine.register_entity(l, "Location", domain='Domain1')

# structure intent
weather_intent = IntentBuilder("WeatherIntent")\
    .require("WeatherKeyword")\
    .optionally("WeatherType")\
    .require("Location")\
    .build()


# define music vocabulary
artists = [
    "third eye blind",
    "the who",
    "the clash",
    "john mayer",
    "kings of leon",
    "adelle"
]

for a in artists:
    engine.register_entity(a, "Artist", domain='Domain2')

music_verbs = [
    "listen",
    "hear",
    "play"
]

for mv in music_verbs:
    engine.register_entity(mv, "MusicVerb", domain='Domain2')

music_keywords = [
    "songs",
    "music"
]

for mk in music_keywords:
    engine.register_entity(mk, "MusicKeyword", domain='Domain2')

music_intent = IntentBuilder("MusicIntent")\
    .require("MusicVerb")\
    .optionally("MusicKeyword")\
    .optionally("Artist")\
    .build()

engine.register_intent_parser(weather_intent, domain='Domain1')
engine.register_intent_parser(music_intent, domain='Domain2')


if __name__ == "__main__":
    for intents in engine.determine_intent(' '.join(sys.argv[1:])):
        print(intents)
