from django.views.generic import ListView, DetailView, CreateView, UpdateView
from movie_list.models import Movie


class MovieCollection(ListView):
    model = Movie
    template_name = 'movie_list/movie_list.html'


class MovieDetailView(DetailView):
    template_name = 'movie_list/movie_detail.html'
    queryset = Movie.objects.all()


class MovieCreateView(CreateView):
    template_name = 'movie_list/add_movie.html'
    model = Movie
    fields = '__all__'


class MovieEditView(UpdateView):
    template_name = 'movie_list/add_movie.html'
    model = Movie
    fields = '__all__'
