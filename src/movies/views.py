from django.views.generic import FormView
from django.shortcuts import redirect
from django.db.models import ObjectDoesNotExist
from movies.forms import SearchMovieForm
from movie_list.models import Movie


class MainPage(FormView):
    template_name = 'home.html'
    form_class = SearchMovieForm

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title', None)
        try:
            pk = Movie.objects.get(title=title).pk
            return redirect('/movie_list/' + str(pk))
        except ObjectDoesNotExist:
            return redirect('/')
