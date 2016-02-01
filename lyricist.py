from lyricist.rpmchain import RGMChain
from lyricist.rapgenius.rgartist import RGArtist
from lyricist.markov.markov_chain import MarkovChain
import argparse, collections, random, re
import pickle

class Program(object):
    """ Command line program"""
    # Yes, it's C#ish, I know

    def __init__(self):
        # Basically just "declaring" variables
        self._artists = None
        self._min_lines = None
        self._max_lines = None
        self._min_verses = None
        self._max_verses = None
        self._min_words = None
        self._max_words = None
        self._seed = None
        self._out_file = None
        self._in_mchain_file = None
        self._load_from_file = None

        self._rpmchain = None

    def positive_int(self, value):
        MSG = "Argument must be a positive integer."
        try:
            arg = int(value)
            if arg > 0:
                return arg
            else:
                raise argparse.ArgumentTypeError(MSG)
        except ValueError:
            raise arparse.ArgumentTypeError(MSG)

    def build_parser(self):
        """Setup and return the argument parser."""
        # Note: the default values don't have a specific reason to have those values
        parser = argparse.ArgumentParser(description="Generate RAP lyrics from your artist, or even make a mixture of them.")
        parser.add_argument("artist", nargs="+", help="artist url(s) or artist name(s). Please note that the artist name case might fail, it's recommended to provide a url.")
        parser.add_argument("-l", "--lines", default=[4, 10], nargs=2, type=self.positive_int, metavar=("MIN_LINES", "MAX_LINES"), help="speciefies the minimum and the maximum amount of lines in each verse. The actual number of lines is chosen randomly from that range for each verse.")
        parser.add_argument("-v", "--verses", default=[3, 10], nargs=2, type=self.positive_int, metavar=("MIN_VERSES", "MAX_VERSES"), help="speciefies the minimum and the maximum amount of verses in the song. The actual number of verses is chosen randomly from that range.")
        parser.add_argument("-w", "--words", default=[5, 10], nargs=2, type=self.positive_int, metavar=("MIN_WORDS", "MAX_WORDS"),help="speciefies the minimum and the maximum amount of words in a line. The actual numer of words in a line is chosen randomly from that range for each line.")
        parser.add_argument("-s", "--seed", help="seed word: the word with each to begin the song. If no value is provided a random one is chosen.")
        parser.add_argument("-o", "--output", metavar="FILE_NAME", help="save song to file. Saves the song to the specified file.")
        parser.add_argument("-m", "--mchain", metavar="FILE_NAME", help="save the created MChain object to file. This later allows to instantiate an artist with that MChain. This is useful because scraping is a relatively lengthy process and saving the scraped content for later use is more convinient than having to re-scrape the whole thing again.")
        parser.add_argument("-f", "--file", default=False, action="store_true", help="instantiate the program with an existing MChain instead of scraping the songs and building a new Markov Chain from them. If this argument is present, the artist arguments are treated as MChain file names [currently only supports one Mchain object].")

        return parser
        
    def parse_args(self):
        """ Parse and process command line args """
        parser = self.build_parser()
        args = parser.parse_args()
        # Bind command line args to global vars
        self._artists = args.artist if isinstance(args.artist, collections.Iterable) else [artist]
        self._min_lines = args.lines[0]
        self._max_lines = args.lines[1]
        self._min_verses = args.verses[0]
        self._max_verses = args.verses[1]
        self._min_words = args.words[0]
        self._max_words = args.words[1]
        self._seed = args.seed
        self._out_file = args.output
        self._out_mchain_file = args.mchain
        self._load_from_file = args.file # boolean

        self._setup_state()

        return self

    def build_chain(self):
        """ Build the Markov Chain for the specified artist(s) 

            If necessary (i.e. if no input MChain object was provided) scrape the necessary song
            lyrics and build a Markov Chain from them.
        """
        if self._load_from_file:
            return self # Markov Chain already loaded, no need to build it
        else:
            self._rgmchain.build_mchain() # this might take a while...
            if self._out_mchain_file is not None:
                # save MChain if needed
                pickle.dump(self._rgmchain.mchain, open(self._out_mchain_file, "wb"))
            return self

    def compose(self):
        """ Composes the song """
        song = ""
        seed = self._seed
        for _ in range(0, random.choice(range(self._min_verses, self._max_verses+1))): # num verses
            for _ in range(random.choice(range(self._min_lines, self._max_lines+1))): # num lines in each verse
                num_words = random.choice(range(self._min_words, self._max_words+1)) # num words in each line
                song += self._rgmchain.generate_sentence(num_words, seed=seed) + "\n"
                seed = None # only use seed (if present for the first sentence)
            song += "\n" # newline at the end of the verse

        return song


    def _setup_state(self):
        """ Sets up the RGMChain instance based on the command line args. """
        if self._load_from_file:
            # load MChain from file, treat artist argumet as file names
            # NOTE: for now only supports a single MChain object
            # TODO: if multiple file names are provided, combine the MChain state maps
            try:
                mchain = pickle.load(open(self._artists[0], "rb"))
            except (IOError, FileNotFoundError) as e:
                print("Error opening file, please make sure that the file exists.")
                print(e)
            self._rgmchain = RGMChain(mchain=mchain)
        else:
            # instantiate RGMChain from artist list
            self._rgmchain = RGMChain(artists=[RGArtist(elem) if self._is_url(elem) else RGArtist.from_artist_name(elem) for elem in self._artists])

        return self

    def _is_url(self, value):
        """ Given a string, returns True if it represents a url, False else """
        return len(re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", value)) > 0

if __name__ == "__main__":
    program = Program()
    program.parse_args()
    program.build_chain()
    song = program.compose()
    print(song)