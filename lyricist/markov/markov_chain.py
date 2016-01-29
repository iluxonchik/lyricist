import random

class MarkovChain(object):
    """ An interface for signle-word states Markov Chains """

    def __init__(self, text=None):
        self._states_map = {}
        if text is not None:
            self.add_text(text)

    def add_text(self, text, separator=" "):
        """ Adds text to the markov chain """
        word_list = text.split(separator)
        for i in range(0, len(word_list)-1):
            self._states_map.setdefault(word_list[i], []).append(word_list[i+1])
        return self

    def add_text_collection(self, text_col, separator=" "):
        """ Adds a collection of text strings to the markov chain """
        for line in text_col:
            if line not in ["", "\n", None]:
                self.add_text(line, separator)


    def get_word(self, key):
        """ Returns a word from Markov Chain associated with the key """
        values = self._states_map.get(key)
        return random.choice(values) if values is not None else None

    def get_random_key(self):
        return random.choice(list(self._states_map.keys()))