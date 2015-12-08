from urllib.request import urlopen
from datetime import date
import json
from bs4 import BeautifulSoup

import culture_filter as cf


def test_recommender():
    r = cf.Recommender()
    assert r.medium == 'all'
    assert r.filename == 'all_mediums.txt'
    assert type(r.recommendations) == dict


def test_album_recommender():
    a = cf.Album()
    assert a.medium == 'albums'
    assert a.filename == 'albums.txt'
    assert type(a.recommendations) == dict


def test_album_load_data():
    try:
        with open('albums.txt', 'r') as infile:
            albums_data = json.load(infile)
    except FileNotFoundError:
        albums_data = {}
    a = cf.Album()
    assert albums_data == a.recommendations


def test_album_save_data():
    a = cf.Album()
    a.save_to_file()
    try:
        with open('albums.txt', 'r') as infile:
            albums_data = json.load(infile)
    except FileNotFoundError:
        albums_data = {}
    assert a.recommendations == albums_data


def test_album_get_ranked_recommendations():
    a = cf.Album()
    ranked_recs = a.get_ranked_recommendations()
    ranked_recs = iter(ranked_recs)
    for album in ranked_recs:
        try:
            # get the rank from the end of the string to compare
            # truthy values
            assert album[-1] >= next(ranked_recs)[-1]
        except StopIteration:
            return

# scraper tests take a while to run. think of how to break them up into variables
# or simplify. or use simple local test html file


def test_publication():
    p = cf.Publication('title', 'https://www.python.org/', 'rank', 'medium')
    assert p.title == 'title'
    assert p.url == 'https://www.python.org/'
    assert p.rank == 'rank'
    assert p.medium == 'medium'
    today = date.today()
    assert p.last_updated == today
    assert p.recommendations == []
    assert p.html is not None


# Utility function for testing that scrapers return correctly formatted
# data


def scraper_test(pub):
    p = pub
    assert p.recommendations == []
    p.scrape()
    assert type(p.recommendations[0]) == tuple
    assert p.recommendations[0][0] is not None

# Tests for individual publications


def test_pitchfork_html():
    p = cf.Pitchfork()
    assert p.html is not None
    scraper_test(p)


def test_pitchfork_songs_html():
    p = cf.PitchforkSongs()
    assert p.html is not None
    scraper_test(p)








