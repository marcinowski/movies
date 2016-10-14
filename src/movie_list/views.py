from django.views.generic import ListView, DetailView
from movie_list.models import Movie


class MovieCollection(ListView):
    model = Movie
    template_name = 'movie_list/movie_list.html'


class MovieDetailView(DetailView):
    template_name = 'movie_list/movie_detail.html'
    queryset = Movie.objects.all()
