from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from .const import constant

class BSOpener(object):
    """ A wrapper arround urllib and BeautifulSoup used a helper for url requests """
    # TODO: make this class a singleton

    class _Const():
        """ Contains the constants used in BSOpener class """
        
        @constant
        def HEADERS():
            """ Headers to send with all url requests """
            return {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"}

    def __init__(self):
        self.CONST = self._Const()

    def bsopen(self, url, headers=None):
        if headers is None:
            headers=self.CONST.HEADERS

        req = Request(url=url, headers=headers)
        try:
            html = urlopen(req)
        except HTTPError:
            print("WARNING: exception during opening url: " + url)
            return None

        return BeautifulSoup(html, "html.parser")
