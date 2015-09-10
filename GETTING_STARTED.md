# Adapt Intent Determination
The Adapt Intent Parser is a flexible and extensible intent definition and determination framework. It is intended to parse natural language text into a structured intent that can then be invoked programmatically. It uses a technique known as known-entity tagging to tag pre-defined vocabulary within utterances. These tags can then be passed to an intent definition for validation. 

## Getting Started
The Parser depends on a tokenizer (splits an utterance into tokens), and a prefix tree loaded with vocabulary. 

        # Instantiate a Trie for in-memory index, a tokenizer, and the entity tagger.
        trie = Trie()
        tokenizer = EnglishTokenizer()
        tagger = EntityTagger(self.trie, self.tokenizer)
        # load vocabulary into index
        trie.insert("play", "PlayVerb")
        trie.insert("the big bang theory", "Television Show")
        trie.insert("the big", "Not a Thing")
        trie.insert("barenaked ladies", "Radio Station")
        # Instantiate parser
        parser = Parser(self.tokenizer, self.tagger)

        # Define intent
        intent = IntentBuilder("play television intent")\
            .require("PlayVerb")\
            .require("Television Show")\
            .build()

        # parser.parse returns a generator, which returns (using a greedy algo) highest confidence parse first, for short-circuiting
        for result in self.parser.parse("play the big bang theory"):
            # validate an intent. A score of 0.0 indicates the parse result is not a valid representation of the intent.
            result_intent = intent.validate(result.get('tags'), result.get('confidence'))
            assert result_intent.get('confidence') > 0.0
            assert result_intent.get('PlayVerb') == 'play'
            assert result_intent.get('Television Show') == "the big bang theory"


