[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE.md) [![CLA](https://img.shields.io/badge/CLA%3F-Required-blue.svg)](https://mycroft.ai/cla) [![Team](https://img.shields.io/badge/Team-Mycroft_Core-violetblue.svg)](https://github.com/MycroftAI/contributors/blob/master/team/Mycroft%20Core.md) ![Status](https://img.shields.io/badge/-Production_ready-green.svg)

[![Build Status](https://travis-ci.org/MycroftAI/adapt.svg?branch=master)](https://travis-ci.org/MycroftAI/adapt) [![Coverage Status](https://coveralls.io/repos/github/MycroftAI/adapt/badge.svg?branch=dev)](https://coveralls.io/github/MycroftAI/adapt?branch=master)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Join chat](https://img.shields.io/badge/Mattermost-join_chat-brightgreen.svg)](https://chat.mycroft.ai)

Adapt Intent Parser
==================
The Adapt Intent Parser is a flexible and extensible intent definition and determination framework. It is intended to parse natural language text into a structured intent that can then be invoked programatically.

[![Introducing the Adapt Intent Parser](https://mycroft.ai/wp-content/uploads/2019/05/Adapt-video-still.png)](https://www.youtube.com/watch?v=zR9xvPtM6Ro)

Getting Started
===============
To take a dependency on Adapt, it's recommended to use virtualenv and pip to install source from github.

```bash
$ virtualenv myvirtualenv
$ . myvirtualenv/bin/activate
$ pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser
```

Examples
========
Executable examples can be found in the [examples folder](https://github.com/MycroftAI/adapt/tree/master/examples).

Intent Modelling
================
In this context, an Intent is an action the system should perform. In the context of Pandora, we’ll define two actions: List Stations, and Select Station (aka start playback)

With the Adapt intent builder:
```Python
list_stations_intent = IntentBuilder('pandora:list_stations')\
    .require('Browse Music Command')\
    .build()
```

For the above, we are describing a “List Stations” intent, which has a single requirement of a “Browse Music Command” entity.

```Python
play_music_command = IntentBuilder('pandora:select_station')\
    .require('Listen Command')\
    .require('Pandora Station')\
    .optionally('Music Keyword')\
    .build()
```


For the above, we are describing a “Select Station” (aka start playback) intent, which requires a “Listen Command” entity, a “Pandora Station”, and optionally a “Music Keyword” entity.

Entities
========

Entities are a named value. Examples include:
`Blink 182` is an `Artist`
`The Big Bang Theory` is a `Television Show`
`Play` is a `Listen Command`
`Song(s)` is a `Music Keyword`

For my Pandora implementation, there is a static set of vocabulary for the Browse Music Command, Listen Command, and Music Keyword (defined by me, a native english speaker and all-around good guy). Pandora Station entities are populated via a "List Stations" API call to Pandora. Here’s what the vocabulary registration looks like.

```Python
def register_vocab(entity_type, entity_value):
    pass
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
```

Development
===========

Glad you'd like to help!

To install test and development requirements run

```
pip install -r test-requirements.txt
```

This will install the test-requirements as well as the runtime requirements for adapt.

To test any changes before submitting them run

```
./run_tests.sh
```

This will run the same checks as the Github actions and verify that your code should pass with flying colours.

Reporting Issues
================
It's often difficult to debug issues with adapt without a complete context. To facilitate simpler debugging,
please include a serialized copy of the intent determination engine using the debug dump
utilities.

```python
from adapt.engine import IntentDeterminationEngine
engine = IntentDeterminationEngine()
# Load engine with vocabulary and parsers

import adapt.tools.debug as atd
atd.dump(engine, 'debug.adapt')
```

Learn More
========

Further documentation can be found at https://mycroft-ai.gitbook.io/docs/mycroft-technologies/adapt
