from collections import OrderedDict
from django.test import TestCase
from django.shortcuts import resolve_url
from django.contrib.auth.models import User
from unittest.mock import patch

from movie_list.models import Movie, Genre, Country, Person


class TestMoviesView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_pwd')
        self.user_2 = User.objects.create_user(username='test_user_2', password='test_pwd')
        self.logged = self.client.login(username='test_user', password='test_pwd')
        self.url = '/'

    def test_user_is_authenticated(self):
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.is_authenticated())
        self.assertTrue(self.logged)

    def test_response_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestCollectionView(TestMoviesView):
    def setUp(self):
        super(TestCollectionView, self).setUp()
        self.url = resolve_url('/movie_list/')
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
        self.movie_2 = Movie.objects.create(title='movie_2', year=1000, user=self.user_2)
        self.movie_1.actors.add(self.person_1)
        self.movie_1.director.add(self.person_2)
        self.movie_1.genre.add(self.genre_1)

    def test_response_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_filtering_by_title(self):
        response = self.client.get(self.url + '?title=movie_1')
        self.assertEqual(len(response.context['object_list']), 1)

    def test_filtering_by_actor(self):
        response = self.client.get(self.url + '?actors=test_person_1')
        self.assertEqual(len(response.context['object_list']), 1)

    def test_filtering_by_director(self):
        response = self.client.get(self.url + '?director=test_person_1')
        self.assertEqual(len(response.context['object_list']), 1)

    def test_filtering_by_genre(self):
        response = self.client.get(self.url + '?genre=comedy')
        self.assertEqual(len(response.context['object_list']), 1)


class TestMovieDetailView(TestMoviesView):
    def setUp(self):
        super(TestMovieDetailView, self).setUp()
        self.movie_1 = Movie.objects.create(title='movie_1', year=2000, user=self.user)
        self.movie_2 = Movie.objects.create(title='movie_2', year=2000, user=self.user_2)
        self.url = resolve_url('/movie_list/{}/'.format(self.movie_1.id))

    def test_response_404_for_movie_out_of_user_db(self):
        url = resolve_url('/movie_list/{}/'.format(self.movie_2.id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_response_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['movie'], self.movie_1)


class TestMovieCreateView(TestMoviesView):
    def setUp(self):
        super(TestMovieCreateView, self).setUp()
        self.url = resolve_url('/movie_list/add/')

    @patch('movie_list.views.OMDBFetcher.page_search', return_value={'title': 'test'})
    def test_search_title(self, mock):
        response = self.client.get(self.url + '?title=test')
        self.assertEqual(response.context['result'], {'title': 'test'})

    @patch('movie_list.views.OMDBFetcher.get', return_value=[{'title': 'test', 'year': 2000}])
    def test_get_title_and_year(self, mock):
        response = self.client.get(self.url + '?title=test&year=2000')
        self.assertEqual(response.context['result'], [{'title': 'test', 'year': 2000}])
        response = self.client.get(self.url + '?title=test&year=2000&form=true')
        self.assertEqual(response.context['result'], [{'title': 'test', 'year': 2000}])
        self.assertEqual(response.context['movie'], {'title': 'test', 'year': 2000})

    @patch('movie_list.views.OMDBFetcher.get', return_value=[{'title': 'test', 'year': 2000}])
    def test_get_imdb_id(self, mock):
        response = self.client.get(self.url + '?imdb_id=1')
        self.assertEqual(response.context['result'], [{'title': 'test', 'year': 2000}])
        response = self.client.get(self.url + '?imdb_id=1&form=true')
        self.assertEqual(response.context['result'], [{'title': 'test', 'year': 2000}])
        self.assertEqual(response.context['movie'], {'title': 'test', 'year': 2000})

    def test_post(self):
        data = {
            'title': 'test_movie',
            'year': 1999,
            'actors': 'actor_test, test_actor',
            'director': 'test_director',
            'genre': 'test_genre, test_genre_2',
            'country': 'test_country',
            'description': 'test_description'
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, resolve_url('/movie_list/'))
        movie = Movie.objects.get(title='test_movie')
        self.assertIsInstance(movie, Movie)
        self.assertEqual(Person.objects.all().count(), 3)
        self.assertEqual(Genre.objects.all().count(), 2)
        self.assertIsInstance(Country.objects.get(name='test_country'), Country)
        self.assertEqual([movie.title, movie.year, movie.description], ['test_movie', 1999, 'test_description'])
        self.assertEqual(movie.user, self.user)


class TestFetchOMDBDataView(TestMoviesView):
    def setUp(self):
        super(TestFetchOMDBDataView, self).setUp()
        self.url = resolve_url('/movie_list/fetch/')

    def test_response_200(self):
        pass

    @patch('movie_list.views.OMDBFetcher.get')
    def test_post(self, mock):
        data = OrderedDict(title='test', year=2000, imdb_id=1)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/movie_list/add/' in response.url)
        self.assertTrue('title=test' in response.url)
        self.assertTrue('year=2000' in response.url)
        self.assertTrue('imdb_id=1' in response.url)


class TestMovieEditView(TestMoviesView):
    def setUp(self):
        super(TestMovieEditView, self).setUp()
        self.movie_1 = Movie.objects.create(title='movie_1', year=2000, user=self.user, id=1)
        self.url = resolve_url('/movie_list/1/edit/')

    def test_get_context(self):
        person_1 = Person.objects.create(name='test_person_1')
        person_2 = Person.objects.create(name='test_person_2')
        genre_1 = Genre.objects.create(name='test_genre_1')
        genre_2 = Genre.objects.create(name='test_genre_2')
        self.movie_1.actors.add(person_1, person_2)
        self.movie_1.director.add(person_1)
        self.movie_1.genre.add(genre_1, genre_2)
        self.movie_1.save()
        response = self.client.get(self.url)
        self.assertEqual(response.context['movie']['genre'], 'test_genre_1, test_genre_2')
        self.assertEqual(response.context['movie']['actors'], 'test_person_1, test_person_2')
        self.assertEqual(response.context['movie']['director'], 'test_person_1')
        self.assertEqual(response.context['movie']['country'], '')

    def test_post(self):
        data = {
            'title': 'movie_1',
            'year': 2000,
            'user': self.user,
            'actors': 'test_person_1, test_person_3',
            'country': 'test_country',
            'metascore': 99
        }
        response = self.client.post(self.url, data=data, user=self.user)
        self.assertEqual(response.status_code, 302)
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.metascore, 99)
        self.assertEqual(Person.objects.count(), 3)
        self.assertEqual(movie.actors.count(), 2)
        self.assertTrue(Person.objects.filter(name='test_person_3').exists())
        self.assertTrue(Country.objects.filter(name='test_country').exists())


class TestMovieDeleteView(TestMoviesView):
    def setUp(self):
        super(TestMovieDeleteView, self).setUp()
        self.movie_1 = Movie.objects.create(title='movie_1', year=2000, user=self.user, id=1)
        self.url = resolve_url('/movie_list/1/delete/')

    def test_response_200(self):
        pass

    def test_delete_model(self):
        self.assertTrue(Movie.objects.filter(title='movie_1').exists())
        self.client.delete(self.url)
        self.assertFalse(Movie.objects.filter(title='movie_1').exists())
