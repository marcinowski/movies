from django.views.generic import ListView
from movie_list.models import Movie


class MovieCollection(ListView):
    model = Movie
    template_name = 'movie_list/movie_list.html'
