import re
from movie_list import models as mov
from omdb.mapping import OMDB_MODEL_MAPPING
from omdb.config import IMDB_MOVIE_BASE_URL


# TODO: generalize resolving fields into db, write tests, handle exceptions with parsing


class OMDBTranslator(object):
    def __init__(self, data):
        self.mapping = OMDB_MODEL_MAPPING
        self.data = data

    def translate(self):
        result = {}
        for key, value in self.data.items():
            new_key = OMDB_MODEL_MAPPING.get(key, '')
            if new_key:
                result.update({new_key: value})
        return self._modify_special_fields(result)

    def _modify_special_fields(self, result):
        self._modify_imdb_url(result)
        return result

    @staticmethod
    def _modify_imdb_url(result):
        imdb_id = result.get('imdb_url', '')
        if imdb_id:
            result['imdb_url'] = IMDB_MOVIE_BASE_URL.format(movie_id=imdb_id)

class OMDBParser(object):
    def __init__(self, data):
        self.mapping = OMDB_MODEL_MAPPING
        self.data = data

    def parse_movie(self):
        obj, _ = mov.Movie.objects.get_or_create(
            title=self._resolve_title_field(),
            description=self._resolve_description_field(),
            year=self._resolve_year_field(),
            icon=self._resolve_icon_field(),
            metascore=self._resolve_metascore_field(),
            imdb_rating=self._resolve_imdb_rating_field(),
            imdb_url=self._resolve_url_field(),
        )
        obj.genre = self._resolve_genre_field()
        obj.director = self._resolve_director_field()
        obj.actors = self._resolve_actors_field()
        obj.country = self._resolve_country_field()

    def _resolve_title_field(self):
        return self.data['Title']

    def _resolve_description_field(self):
        return self.data['Plot']

    def _resolve_icon_field(self):
        return self.data['Poster']

    @staticmethod
    def _parse_int_values(value):
        try:
            return int(value)
        except ValueError:
            pass

    def _resolve_year_field(self):
        try:
            return self._parse_int_values(self.data['Year'])
        except (ValueError, KeyError):
            pass

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
        for obj in objects:
            model.objects.get_or_create(name=obj)
        return model.objects.filter(name__in=objects)

    def _resolve_country_field(self):
        return self._resolve_relational_field(mov.Country, self.data['Country'])

    def _resolve_actors_field(self):
        return self._resolve_relational_field(mov.Person, self.data['Actors'])

    def _resolve_genre_field(self):
        return self._resolve_relational_field(mov.Genre, self.data['Genre'])

    def _resolve_director_field(self):
        return self._resolve_relational_field(mov.Person, self.data['Director'])

    def _resolve_url_field(self):
        return IMDB_MOVIE_BASE_URL.format(movie_id=self.data['imdbID'])

    def _resolve_image_field(self):
        pass
