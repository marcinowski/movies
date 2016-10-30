import urllib.parse

from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.shortcuts import resolve_url, HttpResponseRedirect
from movie_list.models import Movie
from omdb.service import OMDBFetcher
from movie_list.services import MovieService


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

    def get(self, request, *args, **kwargs):
        super(MovieCreateView, self).get(request, *args, **kwargs)
        title = request.GET.get('title', '')
        year = request.GET.get('year', '')
        imdb_id = request.GET.get('imdb_id', '')
        form = request.GET.get('form', '')
        context = self.get_context_data()
        if (title and year) or imdb_id:
            selected_movie = OMDBFetcher().get(title=title, year=year, imdb_id=imdb_id)
            context['result'] = selected_movie
            if form:
                context['selected'] = selected_movie[0]
        elif title:
            context['result'] = OMDBFetcher().page_search(title=title, page=1)
        else:
            context['result'] = []
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', '')
        MovieService().update_or_create(**data)
        return HttpResponseRedirect(resolve_url('movie_list'))


class FetchOMDBDataView(View):
    def post(self, request):
        title = request.POST.get('title', '')
        year = request.POST.get('year', '')
        imdb_id = request.POST.get('imdb_id', '')
        return self._redirect('add_movie', title=title, year=year, imdb_id=imdb_id)

    @staticmethod
    def _redirect(view, **kwargs):
        url = resolve_url(view)
        url += '?' + urllib.parse.urlencode(kwargs)
        return HttpResponseRedirect(url)


class MovieEditView(UpdateView):
    template_name = 'movie_list/add_movie.html'
    model = Movie
    fields = '__all__'
