import requests
import json
from omdb.parser import OMDBTranslator
from omdb.config import OMDB_BASE_URL


class MovieNotFound(Exception):
    pass


class DataDownloadError(Exception):
    pass


class OMDBFetcher(object):
    """
    With this fetcher you can:
    1. Get the data from OMDB either by title and year or by imdb_id,
    2. Search the OMDB page by page with just a title,
    3. Get search results from all the pages.
    Results are always returned in a list.
    """
    def __init__(self):
        self.base_url = OMDB_BASE_URL
        self.session = requests.Session()
        self.translator = OMDBTranslator

    def get(self, title, year='', imdb_id='', d_type='movie'):
        """
        Method for fetching a single movie given by imdb_id or pair title+year.
        :param title: Title of the movie
        :param year: Production year
        :param imdb_id: IMDB id of a movie i.e. tt0368226
        :param d_type: movie or series, just for OMDBAPI
        :return: list with one result
        """
        url = self.base_url + \
            '?t={title}' + \
            '&y={year}' + \
            '&i={imdb_id}' + \
            '&type={type}'
        url = url.format(title=title, year=year, type=d_type, imdb_id=imdb_id)
        response = self.session.get(url)
        if response.ok:
            return self._handle_response(response)
        else:
            raise DataDownloadError('Problem with downloading data.')

    def page_search(self, title, year='', d_type='movie', page=1):
        """
        Method for searching by just one param
        :param title: Title of the movie
        :param year: movie production year
        :param d_type: movie or series, just for OMDBAPI
        :param page: page to return results from
        :return: list of results
        """
        url = self.base_url + \
            '?s={title}' + \
            '&y={year}' + \
            '&type={type}' + \
            '&page={page}'
        url = url.format(title=title, year=year, type=d_type, page=page)
        response = self.session.get(url)
        if response.ok:
            return self._handle_response(response)
        else:
            raise DataDownloadError('Problem with downloading data.')

    def search(self, title, year='', d_type='movie'):
        """
        Method from collecting data from all the search pages.
        :param title: Title of the movie
        :param year: movie production year
        :param d_type: movie or series, just for OMDBAPI
        :return: list of results
        """
        result = []
        page = 1
        while True:
            try:
                content = self.page_search(title, year, d_type, page=page)
            except (MovieNotFound, DataDownloadError):
                break
            else:
                for r in content:
                    result.append(r)
                page += 1
        return result

    def search_generator(self, title, year='', d_type='movie'):
        """
        Method that returns next page search results with each iteration
        :param title: movie title
        :param year: movie production year
        :param d_type: movie or series, just for OMDBAPI
        :return: list of results for consecutive pages
        """
        i = 1
        while True:
            yield self.page_search(title, year, d_type, page=i)
            i += 1

    def _handle_response(self, response):
        content = self._to_python(response)
        self._validate_response(content)
        return self._translate(content)

    @staticmethod
    def _to_python(response):
        try:
            return json.loads(response.content.decode('utf-8'))
        except UnicodeError:
            raise DataDownloadError('Error while decoding response to JSON.')
        except ValueError:
            raise DataDownloadError('Error while converting JSON to python dictionary.')

    @staticmethod
    def _validate_response(content):
        try:
            if content['Response'] != 'True':
                raise MovieNotFound('No movie was found for given search parameters.')
        except KeyError:
            raise DataDownloadError('Incorrect JSON content structure.')

    @staticmethod
    def _translate(content):
        element = content.get('Search', [content])
        return [OMDBTranslator(data).translate() for data in element]
