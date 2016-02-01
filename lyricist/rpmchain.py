from .markov.markov_chain import MarkovChain
from .rapgenius.rgartist import RGArtist
from .text_filter import TextFilter
from .text_filter import Pipeline
from .const import constant
import collections, re

import pickle

class RemoveSqBracketsFilter(TextFilter):
    """ Removes all of the square brackets and its content """
    def apply(self, text):
        return re.sub("\[(.*?)\]", "", text)

class RemoveParensFilter(TextFilter):
    """ Removes parentheses only, keeps their content """
    def apply(self, text):
        return re.sub("\(|\)", "", text)

class AllLowerCaseFilter(TextFilter):
    def apply(self, text):
        return text.lower()

class RGMChain(object):
    """ This is the class responsible for interface between RGArtist and Markov Chains. """
    
    class _Const(object):
        @constant
        def DEFAULT_PIPELINE():
            return Pipeline([RemoveSqBracketsFilter(), RemoveParensFilter(), AllLowerCaseFilter()]) 

    def __init__(self, artists = None,  pip = None, mchain=None):
        self._CONS = self._Const()
        self._artists = artists if artists is not None else [] # list of RGArtist objects
            
        # if a single artist was provided, turn it into a list
        if not isinstance(self._artists, collections.Iterable):
            self._artists = [self._artists]
        
        self._mchain = MarkovChain() if mchain is None else mchain
        self._pipeline = pip if pip is not None else self._CONS.DEFAULT_PIPELINE

    # Properties
    @property
    def mchain(self):
        """ MChain object associated with this instance """
        return self._mchain

    @mchain.setter
    def mchain(self, value):
        self_.machain = value

    @mchain.deleter
    def mchain(self):
        self._mchain = None

    def _build_mchain_for_artist(self, artist, page_limit=None):
        num_pages = 0
        song_urls = artist.get_song_urls(num_pages+1)
        while song_urls is not None:
            # if needed, break due to page limit
            if page_limit is not None:
                if num_pages >= page_limit:
                    break
            song_num = 0
            for song_url in song_urls:
                song_text = artist.get_song_text(song_url)
                filtered_text = self._pipeline.apply(song_text)
                self._mchain.add_text_collection(filtered_text.split("\n"))
                song_num += 1
                print("Song: " + str(song_num))

            num_pages += 1
            song_urls = artist.get_song_urls(num_pages+1)

    def add_filter(self, fil):
        """ Adds a new text filter to the pipeline """
        self._pipeline.add(fil)

    def add_artist(self, artist):
        self._artists.append(artist)
        return self._artists # allows chaining

    def build_mchain(self, page_limit=None):
        """ Build Markov Chain from artist lyrics """
        for artist in self._artists:
            self._build_mchain_for_artist(artist, page_limit)

    def generate_sentence(self, num_words, seed=None, capitalize_first_word=False, end_with_period=False, end_on_nores=False):
        """ Generates and returns a sentence with num_words words, starting with the word seed.

            Keyword arguments:
            seed -- the word with wich to begin the sentence. If no seed word is provided, a random starting word is chosen.
            end_on_nores -- end the sentence and return it, even if less than num_words have been added so far in case the markov
                chain does not have a match for a word.
        """
        if seed is None:
            # select a random staring word
            seed = self._mchain.get_random_key()

        if capitalize_first_word:
            sentence = seed.capitalize()
        else:
            sentence = seed

        word_cnt = 1 # words so far in the sentence
        
        while word_cnt < num_words:
            seed = self._mchain.get_word(seed) # update word (get next word)
            if seed is None:
                if end_on_nores:
                    return sentence
            else:
                seed = self._mchain.get_random_key()

            sentence += " " + seed
            word_cnt += 1
        

        if end_with_period:
            sentence += "."

        return sentence
