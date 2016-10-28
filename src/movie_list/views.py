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
        context = self.get_context_data()
        if title and year:
            context['result'] = [OMDBFetcher().get(title=title)]
        elif title:
            context['result'] = OMDBFetcher()._page_search(title=title, page=1)
        else:
            context['result'] = []
        print(context)
        return self.render_to_response(context)


class FetchOMDBDataView(View):
    def post(self, request):
        title = request.POST.get('title', None)
        year = request.POST.get('year', None)
        return self._redirect('add_movie', title=title, year=year)

    @staticmethod
    def _redirect(view, **kwargs):
        url = resolve_url(view)
        url += '?' + urllib.parse.urlencode(kwargs)
        return HttpResponseRedirect(url)


class MovieEditView(UpdateView):
    template_name = 'movie_list/add_movie.html'
    model = Movie
    fields = '__all__'
