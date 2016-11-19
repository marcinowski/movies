from django.test import TestCase
from django.contrib.auth.models import User
from movie_list.services import MovieService, ManyResultsFoundException
from movie_list.models import Movie, Genre, Person, Country


class TestMovieService(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='test_user', password='test_pwd')
        self.user_2 = User.objects.create_user(username='test_user_2', password='test_pwd')
        self.movie_1 = Movie.objects.create(title='test_movie', year=2000, user=self.user_1)
        self.movie_2 = Movie.objects.create(title='test_movie', year=2016, user=self.user_1)
        self.movie_3 = Movie.objects.create(title='test_movie', year=2016, user=self.user_2)
        self.service = MovieService()

    def test_get(self):
        movie = self.service.get(title='test_movie', year=2000)
        self.assertEqual(movie, self.movie_1)
        with self.assertRaises(ManyResultsFoundException):
            self.service.get(title='test_movie', year=2016)
        movie = self.service.get(title='test_movie', year=2016, user=self.user_1)
        self.assertEqual(movie, self.movie_2)
        with self.assertRaises(ManyResultsFoundException):
            self.service.get(title='test_movie')

    def test_create(self):
        movie = self.service.create(title='test_movie_2', year=2001, user=self.user_1)
        self.assertIsInstance(movie, Movie)

    def test_update_or_create(self):
        self.assertEqual(self.movie_2.imdb_rating, 0.0)
        self.assertEqual(self.movie_2.metascore, 0)
        self.service.update_or_create(
            title='test_movie',
            year=2000,
            user=self.user_1,
            metascore=90,
            imdb_rating=2.3
        )
        movie = self.service.get(title='test_movie', year=2000)
        self.assertEqual(movie.imdb_rating, 2.3)
        self.assertEqual(movie.metascore, 90)
        self.service.update_or_create(
            title='test_movie',
            year=2000,
            user=self.user_1,
            actors='test_actor, actor_tester,acting_tester'
        )
        movie = self.service.get(title='test_movie', year=2000)
        self.assertEqual(movie.actors.count(), 3)

    def test_get_genres(self):
        Genre.objects.create(name='test_genre')
        genre_list = list(MovieService.get_genre_list())
        self.assertEqual(genre_list, ['test_genre'])

    def test_get_actors(self):
        actor_1 = Person.objects.create(name='test_actor')
        actor_2 = Person.objects.create(name='test_actor_2')
        actor_3 = Person.objects.create(name='test_actor_3')
        self.movie_1.actors.add(actor_1, actor_2)
        self.movie_2.actors.add(actor_1)
        self.movie_3.actors.add(actor_1, actor_3)
        actors_list_u1 = list(MovieService.get_actors_list_for_user(self.user_1))
        actors_list_u2 = list(MovieService.get_actors_list_for_user(self.user_2))
        self.assertEqual(actors_list_u1, ['test_actor', 'test_actor_2'])
        self.assertEqual(actors_list_u2, ['test_actor', 'test_actor_3'])

    def test_get_directors(self):
        director_1 = Person.objects.create(name='test_director')
        director_2 = Person.objects.create(name='test_director_2')
        self.movie_1.director.add(director_1)
        self.movie_2.director.add(director_1)
        self.movie_3.director.add(director_1, director_2)
        directors_list_u1 = list(MovieService.get_directors_list_for_user(self.user_1))
        directors_list_u2 = list(MovieService.get_directors_list_for_user(self.user_2))
        self.assertEqual(directors_list_u1, ['test_director'])
        self.assertEqual(directors_list_u2, ['test_director', 'test_director_2'])
