from omdb_fetcher.fetcher import OMDBFetcher
from omdb_fetcher.parser import OMDBParser


class OMDBService(object):
    def __init__(self):
        self.fetcher = OMDBFetcher()
        self.parser = OMDBParser

    def get(self, title, year, **params):
        response = self.fetcher.get(title, year)
        self.parser(response).parse_movie()
