from django.core.exceptions import MultipleObjectsReturned
from movie_list.models import Movie


class ManyResultsFoundException(Exception):
    pass


class MovieService(object):
    @staticmethod
    def create(**params):
        Movie.objects.create(**params)

    @staticmethod
    def get(**params):
        try:
            return Movie.objects.get(**params)
        except MultipleObjectsReturned:
            raise ManyResultsFoundException('Narrow down get parameters')
