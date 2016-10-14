from django.conf.urls import url
from movie_list.views import MovieCollection, MovieDetailView

urlpatterns = [
    url(r'^$', MovieCollection.as_view(), name='movie_list'),
    url(r'^(?P<pk>[0-9]+)/$', MovieDetailView.as_view(), name='movie_list'),
]
