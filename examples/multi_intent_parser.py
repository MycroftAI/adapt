__author__ = 'seanfitz'
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

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

# define vocabulary
weather_keyword = [
    "weather"
]

for wk in weather_keyword:
    trie.insert(wk.lower(), "WeatherKeyword")

weather_types = [
    "snow",
    "rain",
    "wind",
    "sleet",
    "sun"
]

for wt in weather_types:
    trie.insert(wt.lower(), "WeatherType")

locations = [
    "Seattle",
    "San Francisco",
    "Tokyo"
]

for l in locations:
    trie.insert(l.lower(), "Location")

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
    trie.insert(a.lower(), "Artist")

music_verbs = [
    "listen",
    "hear",
    "play"
]

for mv in music_verbs:
    trie.insert(mv.lower(), "MusicVerb")

music_keywords = [
    "songs",
    "music"
]

for mk in music_keywords:
    trie.insert(mk, "MusicKeyword")

music_intent = IntentBuilder("MusicIntent")\
    .require("MusicVerb")\
    .optionally("MusicKeyword")\
    .optionally("Artist")\
    .build()

intent_parsers = [
    weather_intent,
    music_intent
]

if __name__ == "__main__":
    best_intent = None
    for parse_result in parser.parse(' '.join(sys.argv[1:])):
        for intent_parser in intent_parsers:
            intent = intent_parser.validate(parse_result.get('tags'), parse_result.get('confidence'))
            if not best_intent or intent.get('confidence') > best_intent.get('confidence'):
                best_intent = intent

    if best_intent and best_intent.get('confidence') > 0:
        print(json.dumps(parse_result, indent=4))
