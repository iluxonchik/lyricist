import re
from bs4 import BeautifulSoup
from ..const import constant
from ..bsopener import BSOpener

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

        @constant
        def RG_ARTIST_PAGENUM_PREF():
            """ Prefix for page number """
            return "&page="

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
        """ Returns a list of song BeautifulSoup objects 

            The returned list contains the <li>'s of each song, the song url and other info, 
            such as the song title, can be extracted from it.

            Returns:
                list: list of song BeautifulSoup objects if there is at least one song on the page
                None: if there are no songs on the page
        """
        page_url = self.artist_songs + self.CONST.RG_ARTIST_PAGENUM_PREF + str(page_num)
        print("Page url = " + page_url)
        bsObj = self.urlopener.bsopen(page_url)
        song_container = bsObj.find("ul", {"class":["song_list", "primary_list"]})
        
        if song_container is None:
            return None # no songs found on the page
        
        return song_container.findAll("li")

    def _get_song_text_BSObj(self, song_url):
        """ Returns BeautifulSoup object with the lyrics content """
        bsObj = self.urlopener.bsopen(song_url)
        return bsObj.find("lyrics", {"class":"lyrics"}).find("p") if bsObj is not None else None

    def get_song_urls(self, page_num=1):
        """ Return a list of song urls from page page_num.

            Returns:
                list: list of song urls (as strings) if there is at least one song on the page
                None: if there are no songs on the page

        """
        bsObj_list = self._get_songs_BSObj(page_num)
        if bsObj_list is None:
            return None # no songs found on the page

        song_urls = [] # contains the list of song urls found on the page
        # not using list comprehension because we want to filter out None's
        for bsObj in bsObj_list:
            anchor = bsObj.find("a", {"class":"song_link"})
            # make sure that we don't include any None's in our urls list
            if anchor is not None:
                url = anchor.attrs["href"]
                if url is not None:
                    song_urls += [url]

        # we don't want to return empty lists
        return song_urls if len(song_urls) > 0 else None

    def get_songs_title(self, page_num=1):
        """ Return a list of song titles from page page_num.

            Returns:
                list: list of song titles (as strings) if there is at least one song on the page
                None: if there are no songs on the page
        """
        bsObj_list = self._get_songs_BSObj(page_num)
        if bsObj_list is None:
            return None # no songs found on the page

        song_titles = [] # contains the list of song titles found on the page
        # not using list comprehension because we want to filter out None's
        for bsObj in bsObj_list:
            span = bsObj.find("span", {"class":"song_title"})
            # make sure that we don't include any None's or empty strings in our titles list
            if span not in [None, ""]:
                title = span.get_text()
                if title is not None:
                    song_titles += [title]

        # we don't want to return empty lists
        return song_titles if len(song_titles) > 0 else None


    def get_song_text(self, url):
        """ Returns song text as a string """
        result = ""
        bsObj = self._get_song_text_BSObj(url)
        return "".join(bsObj.find_all(text=True)) if bsObj is not None else ""

    def get_song_title(self, url):
        """ Returns song title as a string """
        pass
