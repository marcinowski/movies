from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from movies.forms import SearchMovieForm


class MainPage(FormView):
    template_name = 'home.html'
    form_class = SearchMovieForm

    @method_decorator(login_required(login_url='/users/login/'))
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title', None)
        return redirect('/movie_list/?title=' + title)
