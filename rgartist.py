from bs4 import BeautifulSoup

class RGArtist(object):
    """RapGeniusArtist"""

    def __init__(self, artist_url=None):
        this.artist_url = artist_url

    def get_songs(self, page_num=1):
        """ Return a list of song urls from page page_num """
        pass

    def get_song_text(self, url):
        """ Returns song text as a string """
        pass

    def get_song_title(self, url):
        """ Returns song title as a string """
        pass

    def get_song_BSObj(self, url):
        """ Return BeautifulSoup instance for a song url """
        pass
