from datetime import date
import json

import requests
from bs4 import BeautifulSoup

""" A script that recommends the best new music, movies, books
and tv based on aggregated reviews from a variety of online
publications.

"""


class Recommender:
    """ The Recommender class saves and loads recommendations from
    various publications and sorts them based on the number of favorable
    reviews they have received.

    Attributes:
        medium: The medium of the recommendations as a string.
        filename: The name of the file used for storage as a string.
        recommendations: A data strucutre to store all recommended works
        for this medium.
    """

    # Abstract class attributes for inheritance to various mediums.
    # Is this the correct way to handle this situation in Python?
    medium = ''
    filename = ''

    # in memory representation of recommendations data structure

    # albums = {
    #     'grimes: art angels': {
    #         "title": "Art Angels",
    #         "artist": "Grimes",
    #         "rank": 0,
    #         "last reviewed": "2015-11-22"
    #         "reviewed by": ['Paste Music']
    #     },
    # }

    def __init__(self, recommendations=None):
        """Load recommendation data into recommendations attribute."""
        try:
            self.recommendations = self.load_data()
        except FileNotFoundError:
            self.recommendations = {}

    def load_data(self):
        """ Return all previous recommendation data for this medium."""
        with open(self.filename, 'r') as infile:
                return json.load(infile)

    def save_to_file(self):
        """Save current recommendation data to disk."""
        with open(self.filename, 'w') as outfile:
            json.dump(self.recommendations, outfile)

    def get_ranked_recommendations(self):
        """Return a sorted list of recommendations based on number of
        favorable reviews and priority ranking of publications."""
        recommendations = []
        for k, v in self.recommendations.items():
            recommendations.append((k, v['rank']))
        ranked_recs = sorted(recommendations, key=lambda x: x[1], reverse=True)
        readable_recs = [
            '{}. Score: {}'.format(rec[0].title(), rec[1])
            for rec in ranked_recs
        ]
        return readable_recs


class Album(Recommender):
    """The album recommender class."""
    medium = 'albums'
    filename = 'albums.txt'


class Song(Recommender):
    """The song recommender class."""
    medium = 'songs'
    filename = 'songs.txt'


class Movie(Recommender):
    """The movie recommender class."""
    medium = 'movies'
    filename = 'movies.txt'


class Show(Recommender):
    """The tv show recommender class."""
    medium = 'tv shows'
    filename = 'shows.txt'


class Book(Recommender):
    """The book recommender class."""
    medium = 'books'
    filename = 'books.txt'

# A list to store instances of all publications for batch data processing.
all_publications = []


class Publication:
    """The Publication class stores information and priority ranking of
    each publication and includes methods for scraping recommendations
    from each publication and storing them in the recommendations attribute
    of the various Recommender sub-classes.

    Attributes:
        title: The title of the publication as a human readable string.
        url: The url of the publication as a string.
        rank: The priority ranking of the publication on a scale of 1 to 3.
        medium: The medium of the recommendations as a string.
        last_updated: The date of the last update as a Python date object.
        recommendations: A list to store recommendations for this publication
        with each recommendation stored as a tuple with ('artist', 'work').
        html: The publication's current html as a Beautiful Soup object.
    """

    # Abstract class attributes for inheritance to various publications
    title = ''
    url = ''
    rank = 0
    medium = ''

    def __init__(self, recommendations=None):
        """Get the current data and reset the recommendations list."""
        self.last_updated = date.today()
        self.recommendations = []

    @property
    def html(self):
        """Returns the publication's html as a Beautiful Soup object."""
        try:
            source = requests.get(self.url)
        except ConnectionError as e:
            print('There was a problem connecting to {}. See error message below:'.format(self.title))
            print(e)
        else:
            html = BeautifulSoup(source.text, 'html.parser')
            return html

    # NEEDS MORE TESTS AND REFACTORING BUT APPEARS TO BE WORKING.
    def add_recommendations(self):
        """Adds publication's current recommendations to medium's permanent
        recommendations data structure and saves to disk. If it's a new
        recommendation: add a new entry to the medium.recommendation data
        structure. If it's already been recommended by another publication:
        increment the 'rank' value, update the 'last reviewed' value and
        add this publication to the 'reviewed by' list. If this publication's
        recommendation has already been recorder, but was gathered by the
        scraper, move on to the next recommendation."""
        # Call __init__ here to load current recommendations. Is there a better
        # way to handle this?
        self.medium.__init__()
        for r in self.recommendations:
            work = '{}: {}'.format(r[0].lower(), r[1].lower())
            if work not in self.medium.recommendations:
                self.medium.recommendations[work] = {"title": r[1],
                                                     "artist": r[0],
                                                     "rank": self.rank,
                                                     "last reviewed": str(self.last_updated),
                                                     "reviewed by": []}
                self.medium.recommendations[work]['reviewed by'].append(self.title)
            elif self.title in self.medium.recommendations[work]['reviewed by']:
                pass
            else:
                self.medium.recommendations[work]['rank'] += self.rank
                self.medium.recommendations[work]['last reviewed'] = str(self.last_updated)
                self.medium.recommendations[work]['reviewed by'].append(self.title)
        self.medium.save_to_file()

    # utility methods for scrapers to inherit here. will write more as i write more scrapers

    # I'm having trouble implementing this without making it a static method, but
    # I would really like to reference self, so I can know which scraper is
    # failing.
    @staticmethod
    def catch_scraper_exceptions(scrape):
        """Decorator method to catch scraper exceptions."""
        def exception_catcher(*args, **kwargs):
            try:
                scrape(*args, **kwargs)
            # Will eventually narrow in on specific exceptions, but for
            # now, it's a catch-all to make sure the program keeps running
            # if one of the scrapers fails
            except Exception as e:
                print("""There was a problem with one of your scrapers.
                    See error below:""")
                print(e)
                return
        return exception_catcher


# Music publications


class Pitchfork(Publication):
    """The Pitchfork Music publication class"""
    title = 'Pitchfork: Best New Albums'
    url = "http://pitchfork.com/reviews/best/albums/"
    rank = 3
    medium = Album()

    # def __init__(self, recommendations=None):
    #     self.last_updated = date.today()
    #     self.recommendations = []

    # custom scraper for this pub. other pages on this pub can inherit
    # for different mediums if they have the same page structure
    # returns a tuple with artist and work and adds to self.recommendations

    @Publication.catch_scraper_exceptions
    def scrape(self):
        """A custom web scraper for this publication. Other pages of this
        publication can inherit this method if they have the same html
        structure. Returns a tuple: ('artist', 'work') and adds to
        recommendations list for this publication."""
        reviews = self.html.find_all(class_='info')
        for r in reviews[:10]:
            self.recommendations.append((r.h1.contents[0], r.h2.contents[0]))

# instantiate and add to all_publications for batch processing. could this be
# handled within the class itself?
pitchfork = Pitchfork()
all_publications.append(pitchfork)


class PitchforkSongs(Pitchfork):
    """The Pitchfork Songs publication class"""
    title = 'Pitchfork: Best New Tracks'
    url = "http://pitchfork.com/reviews/best/tracks/"
    medium = Song()

    @Publication.catch_scraper_exceptions
    def scrape(self):
        """A custom web scraper for this publication."""
        reviews = self.html.find_all(class_='info')
        for r in reviews[:5]:
            artist = r.find('span', class_='artist').contents[0].strip()
            artist = artist[:-1]
            title = r.find('span', class_='title').contents[0].strip()
            title = title.strip('"')
            self.recommendations.append((artist, title))

p4k_songs = PitchforkSongs()
all_publications.append(p4k_songs)


class Stereogum(Publication):
    """The Stereogum Music publication class"""
    title = 'Sterogum'
    url = "http://www.stereogum.com/category/franchises/album-of-the-week/"
    rank = 2
    medium = Album()

    def __init__(self, recommendations=None):
        self.last_updated = date.today()
        self.recommendations = []

    @Publication.catch_scraper_exceptions
    def scrape(self):
        """A custom web scraper for this publication."""
        reviews = self.html.find_all('h2')
        for r in reviews[:10]:
            artist = r.contents[0][20:].strip()
            album = str(r.contents[1])[4:-5]
            self.recommendations.append((artist, album))

stereogum = Stereogum()
all_publications.append(stereogum)


class PasteMusic(Publication):
    """The Paste Music publication class"""
    title = 'Paste Magazine: Music'
    url = "http://www.pastemagazine.com/music"
    rank = 1
    medium = Album()

    def __init__(self, recommendations=None):
        self.last_updated = date.today()
        self.recommendations = []

    @Publication.catch_scraper_exceptions
    def scrape(self):
        """A custom web scraper for this publication."""
        reviews = self.html.find_all(class_='nof articles reviews')
        for i in range(1, len(reviews[0].contents), 2):
            # if rating is greater than 8, add to recommendations
            if float(reviews[0].contents[i].contents[5].contents[3].contents[0]) >= 8:
                artist = str(reviews[0].contents[i].contents[3].contents[0])[:-2]
                album = str(reviews[0].contents[i].contents[3].contents[1])[3:-4]
                self.recommendations.append((artist, album))

paste = PasteMusic()
all_publications.append(paste)

# Movie publications


class PasteMovies(PasteMusic):
    """The Paste Movies publication class"""
    title = 'Paste Magazine: Movies'
    url = "http://www.pastemagazine.com/movies"
    rank = 3
    medium = Movie()

    @Publication.catch_scraper_exceptions
    def scrape(self):
        """A custom web scraper for this publication."""
        reviews = self.html.find_all(class_='nof articles reviews')
        for i in range(1, len(reviews[0].contents), 2):
            if float(reviews[0].contents[i].contents[5].contents[3].contents[0]) >= 8:
                # note subtle differences between this and the music page
                movie = str(reviews[0].contents[i].contents[3].contents[0])[3:-4]
                # no director listed here, will need another scraper to get it
                # for now put in an empty string
                self.recommendations.append((movie, ''))

paste_movies = PasteMovies()
all_publications.append(paste_movies)

# TV Publications


class PasteTV(PasteMusic):
    """The Paste TV publication class"""
    title = 'Paste Magazine: TV'
    url = "http://www.pastemagazine.com/tv"
    rank = 3
    medium = Show()

    @Publication.catch_scraper_exceptions
    def scrape(self):
        """A custom web scraper for this publication."""
        reviews = self.html.find_all(class_='nof articles reviews')
        for i in range(1, len(reviews[0].contents), 2):
            if float(reviews[0].contents[i].contents[5].contents[3].contents[0]) >= 8:
                show = str(reviews[0].contents[i].contents[3].contents[0])[3:-4]
                # no show runner listed here, will need another scraper to get it
                # for now put in an empty string
                self.recommendations.append((show, ''))

paste_tv = PasteTV()
all_publications.append(paste_tv)

# Book publications


class PasteBooks(PasteMusic):
    """The Paste Books publication class"""
    title = 'Paste Magazine: Books'
    url = "http://www.pastemagazine.com/books"
    rank = 2
    medium = Book()

    @Publication.catch_scraper_exceptions
    def scrape(self):
        """A custom web scraper for this publication."""
        reviews = self.html.find_all(class_='nof articles reviews')
        # there must be a less convoluted way to do this!
        for i in range(1, len(reviews[0].contents), 2):
            # if rating is greater than 8, add to recommendations
            if float(reviews[0].contents[i].contents[5].contents[3].contents[0]) >= 8:
                book = str(reviews[0].contents[i].contents[3].contents[0])[3:-4]
                author = str(reviews[0].contents[i].contents[3].contents[1][4:])
                self.recommendations.append((book, author))

paste_books = PasteBooks()
all_publications.append(paste_books)

# Module level functions


def scrape_all_and_save():
    """Iterate through all publications to scrape and save new data."""
    for publication in all_publications:
        publication.scrape()
        publication.add_recommendations()


def print_all():
    """Print all recommendations to the console."""
    all_mediums = [Album(), Song(), Movie(), Show(), Book()]
    for medium in all_mediums:
        ranked_recommendations = medium.get_ranked_recommendations()
        print('Recommended {}:\n'.format(medium.medium))
        for recommendation in ranked_recommendations:
            print('\t{}\n'.format(recommendation))


# very basic command line interface for demo purposes. refactor to use dict
def select_command():
    command = input('''Get recommendations for the best new music, movies, books and tv.
Type 'new' to get new recommendations, 'view' to view current recommendations, or
'quit' to exit the program.''')
    return command

if __name__ == '__main__':
    program_running = True
    while program_running:
        command = select_command()
        if command.lower() == 'new':
            print('Looking for new recommendations ...')
            scrape_all_and_save()
            print_all()
        elif command.lower() == 'view':
            print_all()
        elif command.lower() == 'quit':
            program_running = False
        else:
            print('Invalid command. Please try again.')
