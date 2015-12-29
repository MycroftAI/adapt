__author__ = 'seanfitz'
"""
A sample intent that uses a regular expression entity to
extract location from a query

try with the following:
PYTHONPATH=. python examples/regex_intent_parser.py "what's the weather like in tokyo"
"""

import json
import sys
from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine

engine = IntentDeterminationEngine()

# create and register weather vocabulary
weather_keyword = [
    "weather"
]

for wk in weather_keyword:
    engine.register_entity(wk, "WeatherKeyword")

weather_types = [
    "snow",
    "rain",
    "wind",
    "sleet",
    "sun"
]

for wt in weather_types:
    engine.register_entity(wt, "WeatherType")

# create regex to parse out locations
engine.register_regex_entity("in (?P<Location>.*)")

# structure intent
weather_intent = IntentBuilder("WeatherIntent")\
    .require("WeatherKeyword")\
    .optionally("WeatherType")\
    .require("Location")\
    .build()

engine.register_intent_parser(weather_intent)

if __name__ == "__main__":
    for intent in engine.determine_intent(" ".join(sys.argv[1:])):
        if intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
