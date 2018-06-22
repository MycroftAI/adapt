__author__ = 'seanfitz'
"""
A sample intent that uses a fixed vocabulary to extract entities for an intent

try with the following:
PYTHONPATH=. python examples/single_intent_parser.py "what's the weather like in tokyo"
"""
import json
import sys
from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine

engine = IntentDeterminationEngine()

weather_keyword = [
    "weather"
]

engine.register_entity(weather_keyword, "WeatherKeyword")

weather_types = [
    "snow",
    "rain",
    "wind",
    "sleet",
    "sun"
]

engine.register_entity(weather_types, "WeatherType")

locations = [
    "Seattle",
    "San Francisco",
    "Tokyo"
]


engine.register_entity(locations, "Location")

weather_intent = IntentBuilder("WeatherIntent")\
    .require("WeatherKeyword")\
    .optionally("WeatherType")\
    .require("Location")\
    .build()

engine.register_intent_parser(weather_intent)

if __name__ == "__main__":
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
