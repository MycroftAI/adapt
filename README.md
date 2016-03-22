[![Stories in Ready](https://badge.waffle.io/MycroftAI/adapt.png?label=ready&title=Ready)](https://waffle.io/MycroftAI/adapt)
Getting Started
===============
To take a dependency on Adapt, it's recommended to use virtualenv and pip to install source from github.


    $ virtualenv myvirtualenv
    $ . myvirtualenv/bin/activate
    $ pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser


Examples
========
Executable examples can be found in the [examples folder](https://github.com/MycroftAI/adapt/tree/master/examples).

Overview
==================
The Adapt Intent Parser is a flexible and extensible intent definition and determination framework. It is intended to parse natural language text into a structured intent that can then be invoked programatically.

Intent Modelling
================
In this context, an Intent is an action the system should perform. In the context of Pandora, we’ll define two actions: List Stations, and Select Station (aka start playback)

With the Adapt intent builder:

    list_stations_intent = IntentBuilder('pandora:list_stations')\
        .require('Browse Music Command')\
        .build()


For the above, we are describing a “List Stations” intent, which has a single requirement of a “Browse Music Command” entity.


    play_music_command = IntentBuilder('pandora:select_station')\
        .require('Listen Command')\
        .require('Pandora Station')\
        .optionally('Music Keyword')\
        .build()



For the above, we are describing a “Select Station” (aka start playback) intent, which requires a “Listen Command” entity, a “Pandora Station”, and optionally a “Music Keyword” entity.

Entities
========

Entities are a named value. Examples include:
`Blink 182` is an `Artist`
`The Big Bang Theory` is a `Television Show`
`Play` is a `Listen Command`
`Song(s)` is a `Music Keyword`

For my Pandora implementation, there is a static set of vocabulary for the Browse Music Command, Listen Command, and Music Keyword (defined by me, a native english speaker and all-around good guy). Pandora Station entities are populated via a "List Stations" API call to Pandora. Here’s what the vocabulary registration looks like.


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

Learn More
========

Further documentation can be found at https://adapt.mycroft.ai
