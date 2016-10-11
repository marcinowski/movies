import requests
import json

BASE_URL = 'https://www.omdbapi.com/'


class MovieNotFound(Exception):
    pass


class DataDownloadError(Exception):
    pass


class OMDBFetcher(object):
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()

    def get(self, title, year='', d_type='movie', **params):
        url = self.base_url + \
              '?t={title}' + \
              '&y={year}' + \
              '&type={type}'
        url = url.format(title=title, year=year, type=d_type)
        response = self.session.get(url)
        if response.ok:
            return self._handle_response(response)
        else:
            raise DataDownloadError('Problem with downloading data.')

    def search(self, title, year='', d_type='movie'):
        result = []
        page = 1
        while True:
            try:
                content = self._page_search(title, year, d_type, page=page)
                for r in content['Search']:
                    result.append(r)
                page += 1
            except MovieNotFound:
                break
            except KeyError:
                raise Exception('Wrong JSON response content key.')
        return result

    def search_generator(self, title, year='', d_type='movie'):
        i = 1
        while True:
            yield self._page_search(title, year, d_type, page=i)
            i += 1

    def _page_search(self, title, year='', d_type='movie', page=1, **params):
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

    @staticmethod
    def _handle_response(response):
        try:
            content = json.loads(response.content.decode('utf-8'))
            if content['Response'] == 'True':
                return content
            else:
                raise MovieNotFound('No movie was found for given search parameters.')
        except KeyError:
            raise DataDownloadError('Incorrect JSON content structure.')
        except UnicodeError:
            raise DataDownloadError('Error while decoding response to JSON.')
        except ValueError:
            raise DataDownloadError('Error while converting JSON to python dictionary.')
