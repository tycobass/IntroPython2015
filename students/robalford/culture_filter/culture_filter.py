from datetime import date
import json
import requests
from bs4 import BeautifulSoup


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
        readable_recs = ['{}. Rank: {}'.format(rec[0].title(), rec[1]) for rec in ranked_recs]
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

# works in various mediums. hard-coded sample data for albums.
# albums = {
#     'grimes: art angels': {
#         "title": "Art Angels",
#         "artist": "Grimes",
#         "rank": 0,
#         "last reviewed": "2015-11-22"
#     },
#     }

# songs = {}
# tv_shows = {}
# movies = {}
# books = {}

# all_recommendations = [albums, songs, tv_shows, movies, books]


# def load_data(self, filename):
#     try:
#         with open(filename, 'r') as infile:
#             return json.load(infile)
#     except FileNotFoundError:
#         print("You haven't saved any data yet. Let's get started.")


# def save_to_file(self, filename, data):
#     with open(filename, 'w') as outfile:
#         json.dump(data, outfile)


# def get_ranked_recommendations(self, medium):
#     recommendations = []
#     for k, v in medium.items():
#         recommendations.append((k, v['rank']))
#     ranked_recs = sorted(recommendations, key=lambda x: x[1], reverse=True)
#     return ranked_recs

# Web scrapers for various online publications

# a list to store instances of each publication for batch processing
# could this be a class level attribute of Publication?

all_publications = []


class Publication:
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

    def add_recommendations(self):
        for r in self.recommendations:
            work = '{}: {}'.format(r[0].lower(), r[1].lower())
            if work in self.medium.recommendations:
                self.medium.recommendations[work]['rank'] += self.rank
                self.medium.recommendations[work]['last reviewed'] = str(self.last_updated)
            else:
                self.medium.recommendations[work] = {"title": r[1],
                                                     "artist": r[0],
                                                     "rank": self.rank,
                                                     "last reviewed": str(self.last_updated)}
        self.medium.save_to_file()

    # this wont work well because the interface is different for inherited methods
    # def scrape(self, containing_class, artist_div, work_div):
    #     reviews = self.html.find_all(class_=containing_class)
    #     # add conditional code to only add a certain number at a time, as
    #     # in pitchfork scraper below. (if length more than 10, only add 10)
    #     for r in reviews:
    #         self.recommendations.append((r.artist_div.contents[0], r.work_div.contents[0]))

# Instantiate various publications here and append to all_publications

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
    # returns a tuple with artist and work and adds to recommendations list

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
        for r in reviews[:10]:
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

# Run all your scrapers. This may take a while.


def scrape_all_and_save():
    for publication in all_publications:
        publication.scrape()
        publication.add_recommendations()

def get_ew_tv(html):
    shows = []
    grades = html.find_all(class_='gi')
    for show in grades:
        if show.span.contents[0] == 'B+':
            shows.append(show.h2.contents[0][:-11])
    # for some scrapers, you'll need to open links on one page
    # and then move to processing the info on the next page
    return shows

