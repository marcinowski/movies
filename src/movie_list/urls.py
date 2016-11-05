from django.conf.urls import url
from movie_list.views import MovieCollection, MovieDetailView, MovieCreateView, MovieEditView, \
    FetchOMDBDataView, MovieDeleteView

urlpatterns = [
    url(r'^$', MovieCollection.as_view(), name='movie_list'),
    url(r'^(?P<pk>[0-9]+)/$', MovieDetailView.as_view(), name='movie_detail'),
    url(r'^add/$', MovieCreateView.as_view(), name='add_movie'),
    url(r'^fetch/$', FetchOMDBDataView.as_view(), name='fetch_movie'),
    url(r'^(?P<pk>[0-9]+)/edit/$', MovieEditView.as_view(), name='edit_movie'),
    url(r'^(?P<pk>[0-9]+)/delete/$', MovieDeleteView.as_view(), name='delete_view'),
]
