__author__ = 'seanfitz'
"""
A sample intent that uses a regular expression entity to
extract location from a query

try with the following:
PYTHONPATH=. python examples/regex_intent_parser.py "what's the weather like in tokyo"
"""

import json
import sys
import re
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser

tokenizer = EnglishTokenizer()
trie = Trie()
regex_entities = []
tagger = EntityTagger(trie, tokenizer, regex_entities=regex_entities)
parser = Parser(tokenizer, tagger)

# create and register weather vocabulary
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

# create regex to parse out locations
regex_entities.append(re.compile("in (?P<Location>.*)", re.IGNORECASE))

# structure intent
weather_intent = IntentBuilder("WeatherIntent")\
    .require("WeatherKeyword")\
    .optionally("WeatherType")\
    .require("Location")\
    .build()

if __name__ == "__main__":
    for parse_result in parser.parse(" ".join(sys.argv[1:])):
        intent = weather_intent.validate(parse_result.get('tags'), parse_result.get('confidence'))
        if intent.get('confidence') > 0:
            print(json.dumps(parse_result, indent=4))
