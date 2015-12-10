from datetime import date
import json
import requests
from bs4 import BeautifulSoup

"""

A script that recommends the best new music, movies, books and tv based
on reviews from a variety of online publications.

"""

# example of recommendations data structure

# albums = {
#     'grimes: art angels': {
#         "title": "Art Angels",
#         "artist": "Grimes",
#         "rank": 0,
#         "last reviewed": "2015-11-22"
#     },
#     }

"""

The Recommender class saves and loads recommendations, and sorts them
based on the number of favorable reviews they have received.

"""


class Recommender:
    medium = 'all'
    filename = 'all_mediums.txt'

    def __init__(self, recommendations=None):
        try:
            self.recommendations = self.load_data()
        except FileNotFoundError:
            self.recommendations = {}

    def load_data(self):
        with open(self.filename, 'r') as infile:
                return json.load(infile)

    def save_to_file(self):
        with open(self.filename, 'w') as outfile:
            json.dump(self.recommendations, outfile)

    def get_ranked_recommendations(self):
        recommendations = []
        for k, v in self.recommendations.items():
            recommendations.append((k, v['rank']))
        ranked_recs = sorted(recommendations, key=lambda x: x[1], reverse=True)
        readable_recs = ['{}. Score: {}'.format(rec[0].title(), rec[1]) for rec in ranked_recs]
        return readable_recs


class Album(Recommender):
    medium = 'albums'
    filename = 'albums.txt'


class Song(Recommender):
    medium = 'songs'
    filename = 'songs.txt'


class Movie(Recommender):
    medium = 'movies'
    filename = 'movies.txt'


class Show(Recommender):
    medium = 'tv shows'
    filename = 'shows.txt'


class Book(Recommender):
    medium = 'books'
    filename = 'books.txt'


all_publications = []


class Publication:
    # if this is an abstract class (never instantiated), where should these be defined?
    def __init__(self, title, url, rank, medium, recommendations=None):
        self.title = title
        self.url = url
        self.rank = rank
        self.medium = medium
        self.last_updated = date.today()
        self.recommendations = []

    @property
    def html(self):
        source = requests.get(self.url)
        html = BeautifulSoup(source.text, 'html.parser')
        return html

    # call this method to format and add self.recommendations to medium.recommendations
    # and save to disk
    def add_recommendations(self):
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

    # utility methods for scrapers to inherit here. will add as you write scrapers


# Music publications


class Pitchfork(Publication):
    title = 'Pitchfork: Best New Albums'
    url = "http://pitchfork.com/reviews/best/albums/"
    rank = 3
    medium = Album()

    def __init__(self, recommendations=None):
        self.last_updated = date.today()
        self.recommendations = []

    # custom scraper for this pub. other pages on this pub can inherit
    # for different mediums if they have the same page structure
    # returns a tuple with artist and work and adds to self.recommendations

    def scrape(self):
        reviews = self.html.find_all(class_='info')
        for r in reviews[:10]:
            self.recommendations.append((r.h1.contents[0], r.h2.contents[0]))

pitchfork = Pitchfork()
all_publications.append(pitchfork)


class PitchforkSongs(Pitchfork):
    title = 'Pitchfork: Best New Tracks'
    url = "http://pitchfork.com/reviews/best/tracks/"
    medium = Song()

    # needs its own scrape method, different html structrure
    def scrape(self):
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
    title = 'Sterogum'
    url = "http://www.stereogum.com/category/franchises/album-of-the-week/"
    rank = 3
    medium = Album()

    def __init__(self, recommendations=None):
        self.last_updated = date.today()
        self.recommendations = []

    def scrape(self):
        reviews = self.html.find_all('h2')
        for r in reviews[:10]:
            artist = r.contents[0][20:].strip()
            album = str(r.contents[1])[4:-5]
            self.recommendations.append((artist, album))

stereogum = Stereogum()
all_publications.append(stereogum)


class PasteMusic(Publication):
    title = 'Paste Magazine: Music'
    url = "http://www.pastemagazine.com/music"
    rank = 3
    medium = Album()

    def __init__(self, recommendations=None):
        self.last_updated = date.today()
        self.recommendations = []

    # couldnt test because website was struggling
    def scrape(self):
        reviews = self.html.find_all(class_='nof articles reviews')
        # there must be a less convoluted way to do this!
        for i in range(1, len(reviews[0].contents), 2):
            # if rating is greater than 8, add to recommendations
            if float(reviews[0].contents[i].contents[5].contents[3].contents[0]) >= 8:
                artist = str(reviews[0].contents[i].contents[3].contents[0])[:-2]
                album = str(reviews[0].contents[i].contents[3].contents[1])[3:-4]
                self.recommendations.append((artist, album))

paste = PasteMusic()
all_publications.append(paste)


class PasteMovies(PasteMusic):
    title = 'Paste Magazine: Movies'
    url = "http://www.pastemagazine.com/movies"
    medium = Movie()

    def scrape(self):
        reviews = self.html.find_all(class_='nof articles reviews')
        # there must be a less convoluted way to do this!
        for i in range(1, len(reviews[0].contents), 2):
            # if rating is greater than 8, add to recommendations
            if float(reviews[0].contents[i].contents[5].contents[3].contents[0]) >= 8:
                # note subtle differences between this and the music page
                movie = str(reviews[0].contents[i].contents[3].contents[0])[3:-4]
                # no director listed here, will need another scraper to get it
                # for now put in an empty string
                self.recommendations.append((movie, ''))

paste_movies = PasteMovies()
all_publications.append(paste_movies)


class PasteTV(PasteMusic):
    title = 'Paste Magazine: TV'
    url = "http://www.pastemagazine.com/tv"
    medium = Show()

    def scrape(self):
        reviews = self.html.find_all(class_='nof articles reviews')
        # there must be a less convoluted way to do this!
        for i in range(1, len(reviews[0].contents), 2):
            # if rating is greater than 8, add to recommendations
            if float(reviews[0].contents[i].contents[5].contents[3].contents[0]) >= 8:
                # note subtle differences between this and the music page
                show = str(reviews[0].contents[i].contents[3].contents[0])[3:-4]
                # no show runner listed here, will need another scraper to get it
                # for now put in an empty string
                self.recommendations.append((show, ''))

paste_tv = PasteTV()
all_publications.append(paste_tv)


class PasteBooks(PasteMusic):
    title = 'Paste Magazine: Books'
    url = "http://www.pastemagazine.com/books"
    medium = Book()

    def scrape(self):
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


# Run all your scrapers. This may take a while.
def scrape_all_and_save():
    for publication in all_publications:
        publication.scrape()
        publication.add_recommendations()


# print all recommendations to the console
def print_all():
    all_mediums = [Album(), Song(), Movie(), Show(), Book()]
    for medium in all_mediums:
        # make a new instance to load the latest data
        # medium = medium()
        ranked_recommendations = medium.get_ranked_recommendations()
        print('Recommended {}:\n'.format(medium.medium))
        for recommendation in ranked_recommendations:
            print('\t{}\n'.format(recommendation))

if __name__ == '__main__':
    while True:
        select = input('''Get recommendations for the best new music, movies, books and tv.
Type 'new' to get new recommendations. Type 'view' to view current recommendations.''')
        if select == 'new':
            print('Looking for new recommendations ...')
            scrape_all_and_save()
            print_all()
        elif select == 'view':
            print_all()
        else:
            print('You entered an invalid command.')



# def get_ew_tv(html):
#     shows = []
#     grades = html.find_all(class_='gi')
#     for show in grades:
#         if show.span.contents[0] == 'B+':
#             shows.append(show.h2.contents[0][:-11])
#     # for some scrapers, you'll need to open links on one page
#     # and then move to processing the info on the next page
#     return shows

