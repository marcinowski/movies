import re
import PIL
from movie_list import models as mov
from omdb_fetcher.mapping import OMDB_MODEL_MAPPING


class OMDBParser(object):
    def __init__(self, data):
        self.mapping = OMDB_MODEL_MAPPING
        self.data = data

    def parse_movie(self):
        obj, _ = mov.Movie.objects.get_or_create(
            title=self._resolve_title_field(),
            description=self._resolve_description_field(),
            year=self._resolve_year_field(),
            # metascore=self._resolve_metascore_field(),
            # imdb_rating=self._resolve_imdb_rating_field(),
            # imdb_url=self._resolve_url_field(),
            # country=self._resolve_country_field
            # **self._resolve_text_fields()
        )

        # genre = self._resolve_genre_field(),
        # director = self._resolve_director_field(),
        # actors = self._resolve_actors_field(),

    # def _resolve_text_fields(self):
    #     return {
    #         self.mapping[key]: value for key, value in self.data if self.mapping[key]
    #     }

    def _resolve_title_field(self):
        return self.data['Title']

    def _resolve_description_field(self):
        return self.data['Plot']

    @staticmethod
    def _parse_int_values(value):
        return int(value)

    def _resolve_year_field(self):
        return self._parse_int_values(self.data['Year'])

    def _resolve_metascore_field(self):
        return self._parse_int_values(self.data['Metascore'])

    @staticmethod
    def _parse_float_values(value):
        return float(value)

    def _resolve_imdb_rating_field(self):
        return self._parse_float_values(self.data['imdbRating'])

    @staticmethod
    def _parse_multivalue_field(value):
        return re.split(r',[ ]?', value)

    def _resolve_relational_field(self, model, value):
        objects = self._parse_multivalue_field(value)
        return [
            model.objects.get_or_create(name=obj) for obj in objects
        ]

    def _resolve_country_field(self):
        return self._resolve_relational_field(mov.Country, self.data['Country'])

    def _resolve_actors_field(self):
        return self._resolve_relational_field(mov.Person, self.data['Actors'])

    def _resolve_genre_field(self):
        return self._resolve_relational_field(mov.Genre, self.data['Genre'])

    def _resolve_director_field(self):
        return self._resolve_relational_field(mov.Person, self.data['Director'])

    def _resolve_url_field(self):
        return 'http://www.imdb.com/title/{}/'.format(self.data['imdbID'])

    def _resolve_image_field(self):
        pass
