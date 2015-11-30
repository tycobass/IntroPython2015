from urllib.request import urlopen
from datetime import date
from bs4 import BeautifulSoup

import culture_filter

# class Publication:
#     def __init__(self, title, url, rank, recommendations=None):
#         self.title = title
#         self.url = url
#         self.rank = rank
#         self.last_updated = date.today()
#         self.recommendations = []

#     @property
#     def html(self):
#         source = urlopen(self.url)
#         html = BeautifulSoup(source.read(), 'html.parser')
#         return html

#     def add_recommendations(self, medium):
#         for r in self.recommendations:
#             key = '{}: {}'.format(r[0].lower(), r[1].lower())
#             if key in medium:
#                 medium[key]['rank'] += self.rank
#                 medium[key]['last reviewed'] = self.last_updated
#             else:
#                 medium[key] = {"title": r[1],
#                                "artist": r[0],
#                                "rank": self.rank,
#                                "last reviewed": self.last_updated}

#     # generic scraper methods that will be useful to all publications
#     # for some pubs, these are all you need, so you can instantiate as
#     # instances of Publication class, rather than inheriting
#     def scrape_target_div(self, html, target_div):
#         return html.target_div.contents[0]

# # Music publications


# class Pitchfork(Publication):
#     title = 'Pitchfork: Best New Albums'
#     url = "http://pitchfork.com/reviews/best/albums/"
#     rank = 3

#     def __init__(self, recommendations=None):
#         self.last_updated = date.today()
#         self.recommendations = []

#     # custom scraper for this pub. other pages on this pub can inherit
#     # for different mediums if they have the same page structure
#     def scrape(self):
#         reviews = self.html.find_all(class_='info')
#         for r in reviews[:5]:
#             self.recommendations.append((r.h1.contents[0], r.h2.contents[0]))


# class PitchforkSongs(Pitchfork):
#     title = 'Pitchfork: Best New Tracks'
#     url = "http://pitchfork.com/reviews/best/tracks/"

#     # needs its own scrape method, different html structrure
#     def scrape(self):
#         reviews = self.html.find_all(class_='info')
#         for r in reviews[:5]:
#             artist = r.find('span', class_='artist').contents[0].strip()
#             artist = artist[:-1]
#             title = r.find('span', class_='title').contents[0].strip()
#             title = title.strip('"')
#             self.recommendations.append((artist, title))


# def get_ew_tv(html):
#     shows = []
#     grades = html.find_all(class_='gi')
#     for show in grades:
#         if show.span.contents[0] == 'B+':
#             shows.append(show.h2.contents[0][:-11])
#     # for some scrapers, you'll need to open links on one page
#     # and then move to processing the info on the next page
#     return shows
