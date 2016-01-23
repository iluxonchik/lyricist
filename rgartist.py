import re
from bs4 import BeautifulSoup
from const import constant
from bsopener import BSOpener

class RGArtist(object):
    """RapGeniusArtist"""

    class _Const(object):
        """ Contains constants used in outter class """
        @constant
        def RG_ARTIST_BASE_URL():
            return "http://genius.com/artists/"

        @constant
        def RG_ARTIST_SONGS_BASE_URL():
            return "http://genius.com/artists/songs?for_artist_page="

    def __init__(self, artist_url):
        self.CONST = self._Const()
        self.urlopener = BSOpener()
        self.artist_url = artist_url
        self.artist_id = self._get_artist_id(self.artist_url) # numerical artist id
        self.artist_songs = self.CONST.RG_ARTIST_SONGS_BASE_URL + self.artist_id

    @classmethod
    def from_artist_name(cls, artist_name):
        """ Returns a new instance of RGArtist from artist name 

            Assumes that the artist url is in the form 
            http://genius.com/artists/<artist_name>, where 
            <artist_name> is the artist_name provided as an 
            argument with spaces replaced by "-" and "." removed. This method might return
            a bogus url, since RapGenius doesn't seem to be following any convention for
            the names (for example, sometimes "." in names simply get removed, while in
            other instances they get replaced by "-").
        """
        return RGArtist(cls._Const().RG_ARTIST_BASE_URL + artist_name.replace(" ", "-").replace(".", ""))

    def _get_artist_id(self, artist_url):
        """ Returns the numeric id of the artist """
        bsObj = self.urlopener.bsopen(artist_url)
        content_val = bsObj.find("meta", {"property":"twitter:app:url:iphone"}).attrs["content"]
        return re.findall("[0-9]+$", content_val)[0]

    def _get_songs_BSObj(self, page_num=1):
        return bsObj

    def get_songs(self, page_num=1):
        """ Return a list of song urls from page page_num.

            Returns:
                list: list of song urls if there is at least one song on the page
                None: if there are no songs on the page

        """
        pass

    def get_song_text(self, url):
        """ Returns song text as a string """
        pass

    def get_song_title(self, url):
        """ Returns song title as a string """
        pass

    def get_song_text_BSObj(self, url):
        """ Return BeautifulSoup instance for a song url """
        pass
