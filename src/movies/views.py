from django.views.generic import FormView
from django.shortcuts import redirect
from movies.forms import SearchMovieForm


class MainPage(FormView):
    template_name = 'home.html'
    form_class = SearchMovieForm

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title', None)
        return redirect('/movie_list/?title='+title)
