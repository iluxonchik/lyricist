from lyricist import rpmchain
from lyricist.rapgenius.rgartist import RGArtist
from lyricist.markov.markov_chain import MarkovChain
import argparse
import pickle

def positive_int(value):
    MSG = "Argument must be a positive integer."
    try:
        arg = int(value)
        if arg > 0:
            return arg
        else:
            raise argparse.ArgumentTypeError(MSG)
    except ValueError:
        raise arparse.ArgumentTypeError(MSG)
     
def build_parser():
    """Setup and return the argument parser."""
    # Note: the default values don't have a specific reason to have those values
    parser = argparse.ArgumentParser(description="Generate RAP lyrics from your artist, or even make a mixture of them.")
    parser.add_argument("aritst", nargs="+", help="artist url(s) or artist name(s). Please note that the artist name case might fail, it's recommended to provide a url.")
    parser.add_argument("-l", "--lines", default=[4, 10], nargs=2, type=positive_int, metavar=("MIN_LINES", "MAX_LINES"), help="speciefies the minimum and the maximum amount of lines in each verse. The actual number of lines is chosen randomly from that range for each verse.")
    parser.add_argument("-v", "--verses", default=[3, 10], nargs=2, type=positive_int, metavar=("MIN_VERSES", "MAX_VERSES"), help="speciefies the minimum and the maximum amount of verses in the song. The actual number of verses is chosen randomly from that range.")
    parser.add_argument("-w", "--words", default=[5, 10], nargs=2, type=positive_int, metavar=("MIN_WORDS", "MAX_WORDS"),help="speciefies the minimum and the maximum amount of words in a line. The actual numer of words in a line is chosen randomly from that range for each line.")
    parser.add_argument("-s", "--seed", help="seed word: the word with each to begin the song. If no value is provided a random one is chosen.")

    return parser

if __name__ == "__main__":
    parser = build_parser()
    parser.parse_args()