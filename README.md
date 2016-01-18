Getting Started
===============
To install all dependencies for Adapt, it's recommended to use virtualenv and
pip to install the source from github.


    $ virtualenv myvirtualenv
    $ . myvirtualenv/bin/activate
    $ pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser


Examples
========
Executable examples can be found in the
[examples folder](https://github.com/MycroftAI/adapt/tree/master/examples).

Overview
==================
The Adapt Intent Parser is a flexible and extensible intent definition and
determination framework. It is intended to parse natural language text into a
structured intent that can then be invoked programatically.

Intent Modelling
================
In this context, an Intent is an action the system should perform. In the
context of Pandora, we will define two actions: "List Stations", and "Select
Station" (aka start to play).

We are using the Adapt intent builder to define first the "List Stations"
intent, with a single requirement of a "Browse Music Command" entity.

~~~ python
list_stations_intent = IntentBuilder('pandora:list_stations')\
    .require('Browse Music Command')\
    .build()
~~~

The more complex "Select Station" intent requires a "Listen Command", a
"Pandora Station" and optionally a "Music Keyword" entity.

~~~ python
play_music_command = IntentBuilder('pandora:select_station')\
    .require('Listen Command')\
    .require('Pandora Station')\
    .optionally('Music Keyword')\
    .build()
~~~

Entities
========

Entities are a named value, and work as the building blocks of the intents.
Some examples could be:
  
"Blink 182" is an Artist  
"The Big Bang Theory" is a Television Show  
"Play" is a Listen Command  
"Song(s)" is a Music Keyword  

For the Pandora example implementation, there is a static set of vocabulary for
the "Browse Music" Command, "Listen" Command, and "Music Keyword" (defined by
me, a native english speaker and all-around good guy). Pandora Station entities
are populated via a "List Stations" API call to Pandora. Here’s what the
vocabulary registration looks like.


~~~ python
def register_vocab(entity_type, entity_value):
    # a tiny bit of code 

def register_pandora_vocab(emitter):
    for v in ["stations"]:
        register_vocab('Browse Music Command', v)

    for v in ["play", "listen", "hear"]:
        register_vocab('Listen Command', v)

    for v in ["music", "radio"]:
        register_vocab('Music Keyword', v)

    for v in ["Pandora"]:
        register_vocab('Plugin Name', v)

    station_name_regex = re.compile(r"(.*) Radio")
    p = get_pandora()
    for station in p.stations:
        m = station_name_regex.match(station.get('stationName'))
        if not m:
            continue
        for match in m.groups():
            register_vocab('Pandora Station', match)
~~~
