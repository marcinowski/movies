from django.conf.urls import url
from movie_list.views import MovieCollection

urlpatterns = [
    url(r'^$', MovieCollection.as_view(), name='movie_list'),
]
