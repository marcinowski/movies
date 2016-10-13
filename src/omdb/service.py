from omdb.fetcher import OMDBFetcher
from omdb.parser import OMDBParser


class OMDBService(object):
    def __init__(self):
        self.fetcher = OMDBFetcher()
        self.parser = OMDBParser

    def get(self, title, year, **params):
        response = self.fetcher.get(title, year)
        self.parser(response).parse_movie()
