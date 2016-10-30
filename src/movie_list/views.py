import urllib.parse

from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.shortcuts import resolve_url, HttpResponseRedirect
from movie_list.models import Movie
from omdb.service import OMDBFetcher


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
        context = self.get_context_data()
        if (title and year) or imdb_id:
            context['result'] = OMDBFetcher().get(title=title, year=year, imdb_id=imdb_id)
        elif title:
            context['result'] = OMDBFetcher().page_search(title=title, page=1)
        else:
            context['result'] = []
        return self.render_to_response(context)


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
