import urllib.parse

from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import resolve_url, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from movie_list.models import Movie, Genre
from omdb.service import OMDBFetcher
from omdb.fetcher import MovieNotFound
from movie_list.services import MovieService
from movie_list.mapping import LIST_VIEW_MAPPING


class MovieCollection(ListView):
    model = Movie
    template_name = 'movie_list/movie_list.html'

    def get_queryset(self):
        query = {
            LIST_VIEW_MAPPING[key]: value for key, value in self.request.GET.dict().items() if value
            }
        query['user'] = self.request.user
        queryset = super(MovieCollection, self).get_queryset()
        return queryset.filter(**query)

    def get_context_data(self, **kwargs):
        context = super(MovieCollection, self).get_context_data(**kwargs)
        username = self.request.user
        context['genres'] = Genre.objects.all().values_list('name', flat=True)
        context['directors'] = Movie.objects.filter(user=username).values_list('director__name', flat=True).distinct()
        context['actors'] = Movie.objects.filter(user=username).values_list('actors__name', flat=True).distinct()
        return context


class MovieDetailView(DetailView):
    template_name = 'movie_list/movie_detail.html'
    model = Movie

    def get_queryset(self):
        queryset = super(MovieDetailView, self).get_queryset()
        user = self.request.user
        return queryset.filter(user=user)


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
            try:
                selected_movie = OMDBFetcher().get(title=title, year=year, imdb_id=imdb_id)
            except MovieNotFound:
                context['alert'] = 'No movie was found for given parameters. Check the data or try filling form.'
            else:
                context['result'] = selected_movie
                if form:
                    context['movie'] = selected_movie[0]
        elif title:
            context['result'] = OMDBFetcher().page_search(title=title, page=1)
        else:
            context['result'] = []
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', '')
        data['user'] = self.request.user
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
    template_name = 'movie_list/edit_movie.html'
    model = Movie
    fields = '__all__'

    def get_queryset(self):
        queryset = super(MovieEditView, self).get_queryset()
        user = self.request.user
        return queryset.filter(user=user)


class MovieDeleteView(DeleteView):
    template_name = 'movie_list/delete_movie.html'
    success_url = reverse_lazy('movie_list')
    model = Movie

    def get_queryset(self):
        queryset = super(MovieDeleteView, self).get_queryset()
        user = self.request.user
        return queryset.filter(user=user)

