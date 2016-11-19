import re
from django.core.exceptions import MultipleObjectsReturned
from movie_list.models import Movie, Person, Genre, Country


class ManyResultsFoundException(Exception):
    pass


class MovieService(object):
    @staticmethod
    def create(**params):
        return Movie.objects.create(**params)

    @staticmethod
    def get(**params):
        try:
            return Movie.objects.get(**params)
        except MultipleObjectsReturned:
            raise ManyResultsFoundException('Narrow down get parameters')

    def update_or_create(self, title, year, user, **params):
        genre = self._resolve_relational_field(Genre, params.pop('genre', ''))
        actors = self._resolve_relational_field(Person, params.pop('actors', ''))
        director = self._resolve_relational_field(Person, params.pop('director', ''))
        country = self._resolve_relational_field(Country, params.pop('country', ''))
        obj, _ = Movie.objects.update_or_create(title=title, year=year, user=user, defaults=params)
        obj.genre = genre
        obj.actors = actors
        obj.director = director
        obj.country = country

    @staticmethod
    def get_genre_list():
        return Genre.objects.all().values_list('name', flat=True)

    @staticmethod
    def get_actors_list_for_user(user):
        return Person.objects.filter(actors__user=user).distinct().values_list('name', flat=True)

    @staticmethod
    def get_directors_list_for_user(user):
        return Person.objects.filter(director__user=user).distinct().values_list('name', flat=True)

    @staticmethod
    def _resolve_relational_field(model, values):
        objects = re.split(r',[ ]?', values)
        for obj in objects:
            model.objects.get_or_create(name=obj)
        return model.objects.filter(name__in=objects)
