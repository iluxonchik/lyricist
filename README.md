# Lyricist

Lyricist is where RAP lyrics and Markov Chains meet together. The idea is simple:
scrape Rap Genius for song lyrics, build a Markov Chain from them and then use it
to generate new lyrics.

This is just a toy project created for fun, specifically with the goal of generating
lyrics using [Markov Chains](https://en.wikipedia.org/wiki/Markov_chain) built from 
all of the artist's lyrical content, *i.e* from all of his songs. The fun part is that 
the ouptup should be a song wich, at least minimally, reassembles the artit's style
You can even mix artists to create a "hybrid" and genereate songs which are now influenced
by a group of artists.

All of the songs text is scraped directly from [Rap Genius](http://rap.genius.com/), the songs are
then filtered(for examlple, remove the `[Verse X]` strings) and used to build Markov Chains.

# Usage

To generate a song based on a specific artist (or a mixture of artists) lyrics type the following
at the root of the project:

`python lyricist.py [-h] [-l MIN_LINES MAX_LINES] [-v MIN_VERSES MAX_VERSES] [-w MIN_WORDS MAX_WORDS] [-s SEED] [-o FILE_NAME][-m FILE_NAME] [-f] artist [artist ...]`

This will genrate a song with the sepecified options. Please note that scraping all of the artists lytics might take
some time.

It's usually a good idea to use the `-m FILE_NAME` option, specially if you plan on using the artist(s) to generate more than one
song. `-m FILE_NAME` saves the `Markov Chain` object to disk using `pickle` and later on you can use that object to instiate your `RGArtist`,
which means that you won't have to scrape Rap Genius for lyrics, since you can directly use the states map from the `Markov Chain` object.

To generate a song using a prevoiously saved `Markov Chain` object supply the `-f` and **the artist argument will be treated as the file name containing the Markov Chain object**.

## Example

To generate a song having between 3 and 7 `verses` based on `The Game`'s lyrics starting with the word `Dre`, save the 
`Markov Chain` object for later use and save the song to a file you would run:

`python lyricist.py "The Game" -v 3 7 -s Dre -m the_game.mchain -o song.txt`

To later use the saved `Markov Chain` object to generate another song, save it to a file, this time with a random seed word and the default 
values for all other optional parameters you would run:

`python lyricist.py the_game.mchain -f -o song.txt`

## Detailed Usage

```
usage: lyricist.py [-h] [-l MIN_LINES MAX_LINES] [-v MIN_VERSES MAX_VERSES]
                   [-w MIN_WORDS MAX_WORDS] [-s SEED] [-o FILE_NAME]
                   [-m FILE_NAME] [-f]
                   artist [artist ...]

Generate RAP lyrics from your artist, or even make a mixture of them.

positional arguments:
  artist                artist url(s) or artist name(s). Please note that the
                        artist name case might fail, it's recommended to
                        provide a url.

optional arguments:
  -h, --help            show this help message and exit
  -l MIN_LINES MAX_LINES, --lines MIN_LINES MAX_LINES
                        speciefies the minimum and the maximum amount of lines
                        in each verse. The actual number of lines is chosen
                        randomly from that range for each verse.
  -v MIN_VERSES MAX_VERSES, --verses MIN_VERSES MAX_VERSES
                        speciefies the minimum and the maximum amount of
                        verses in the song. The actual number of verses is
                        chosen randomly from that range.
  -w MIN_WORDS MAX_WORDS, --words MIN_WORDS MAX_WORDS
                        speciefies the minimum and the maximum amount of words
                        in a line. The actual numer of words in a line is
                        chosen randomly from that range for each line.
  -s SEED, --seed SEED  seed word: the word with each to begin the song. If no
                        value is provided a random one is chosen.
  -o FILE_NAME, --output FILE_NAME
                        save song to file. Saves the song to the specified
                        file.
  -m FILE_NAME, --mchain FILE_NAME
                        save the created MChain object to file. This later
                        allows to instantiate an artist with that MChain. This
                        is useful because scraping is a relatively lengthy
                        process and saving the scraped content for later use
                        is more convinient than having to re-scrape the whole
                        thing again.
  -f, --file            instantiate the program with an existing MChain
                        instead of scraping the songs and building a new
                        Markov Chain from them. If this argument is present,
                        the artist arguments are treated as MChain file names
                        [currently only supports one Mchain object].
```

## Notes

Please note that using **artist's url**, instead of the artist's name as the argument to the command line tool
is **recommended**. This is due to the fact that Rap Genius doesn't seem to have a well defined standart for 
artist name urls. Under the hood, the program assumes that the artist url is in the form `http://genius.com/artists/<artist_name>`, 
where `<artist_name>` is the artist_name provided as an argument with spaces replaced by "-" and "." removed. 
This result in an invalid url, since as mentioned previously, Rap Genius doesn't seem to be following any 
convention for the names (for example, sometimes "." in names simply get removed, while in other instances they get 
replaced by "-"). For example if `<artist_name> = "The Game`, this will result in the artist url `http://genius.com/artists/The-Game`.

# Filters

Sometimes you might notice that the output song contains some garbage, like non-alphanumeric symbols. This is due to the fact
that some songs on Rap Genius contains them, sometimes they're typos, sometimes they're intentional (like the `{?}`, when 
people are unsure about what the artist said).

Before building the `Markov Chain`, each one of songs gets **filtered**. For that, sublcasses of `lyricist.text_filter.TextFilter`
are used. This class contains a single method: `apply()` and all it does is recieves a string of text and return another string of text
(*i.e.* it recieves the unfiltered text, filters it as necessary, and then returns the filtered version, which will later might be subject
to more filtering before being used to build the Markov Chain). Filters are combined into a `Pipeline` (`lyricist.text_filter.Pipeline`), which
is simply a collection of `TextFilter`s. The default list of `TextFilters` includes(all defined in the `lyricist/rpmchain.py`): 
`RemoveSqBracketsFilter` (removes all of the squre brackets and the content between them from the text), 
`RemoveParensFilter` (removes the parentheses from text, leaving the content in between them) and `AllLowerCaseFilter` (makes all the text
lowercase). You can easily extend the filter list used and make the output cleaner. Adding a new text filter is as easy as 
calling the `add_filter()` on a `RGMChain` object and supplying a `TextFilter` sublcalss as the argument.

# Requirements

* **Python 3** (any `3.x` version should work)

To run the project you'll need a couple of libraries, actually I take that back, this project only uses one external
dependency:

* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)
    If you have [pip](https://pip.pypa.io/en/stable/) installed, getting Beautiful Soup 4 is as 
    simple as: `pip install beautifulsoup4`
