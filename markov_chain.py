from random import choice

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

    def get_word(self, key):
        """ Returns a word from Markov Chain associated with the key """
        values = self._states_map.get(key)
        return choice(values) if values is not None else None
