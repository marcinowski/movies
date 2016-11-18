from django.test import TestCase
from django.shortcuts import resolve_url
from django.contrib.auth.models import User
from movie_list.models import Movie, Genre, Country, Person


class TestCollectionView(TestCase):
    def setUp(self):
        self.url = resolve_url('/movie_list/')
        self.user = User.objects.create_user(username='test_user', password='test_pwd')
        self.client.login(username='test_user', password='test-pwd')
        self.person_1 = Person.objects.create(name='test_person_1')
        self.person_2 = Person.objects.create(name='test_person_2')
        self.genre_1 = Genre.objects.create(name='comedy')
        self.genre_2 = Genre.objects.create(name='drama')
        self.movie_1 = Movie.objects.create(title='movie_1', year=2000, user=self.user)
        self.movie_1.actors.add(self.person_1)
        self.movie_1.director.add(self.person_2)
        self.movie_1.genre.add(self.genre_1)
        self.movie_2 = Movie.objects.create(title='movie_2', year=1000, user=self.user)
        self.movie_2.actors.add(self.person_2)
        self.movie_2.director.add(self.person_1)
        self.movie_2.genre.add(self.genre_2)

    def test_user_is_authenticated(self):
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.is_authenticated)

    def test_response_200(self):
        response = self.client.get(self.url)
        self.assertTrue(response.ok)
        self.assertEqual(len(response['movie']), 2)

    def test_filtering_by_title(self):
        response = self.client.get(self.url + '?title=movie_1')
        self.assertEqual(len(response['movie']), 1)

    def test_filtering_by_actor(self):
        response = self.client.get(self.url + '?actors=person_1')
        self.assertEqual(len(response['movie']), 1)

    def test_filtering_by_genre(self):
        response = self.client.get(self.url + '?genre=comedy')
        self.assertEqual(len(response['movie']), 1)
