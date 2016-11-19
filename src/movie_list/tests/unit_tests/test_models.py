from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from movie_list.models import Movie, Genre, Person, Country


class TestSingleNameModel(TestCase):
    def test_repr(self):
        tests = {
            'test_genre': Genre,
            'test_person': Person,
            'test_country': Country
        }
        for name, model in tests.items():
            instance = model.objects.create(name=name)
            self.assertEqual(str(instance), name)


class TestMovieModel(TestCase):
    def setUp(self):
        self.genres = [Genre.objects.create(name='genre_' + str(no)) for no in range(2)]
        self.people = [Person.objects.create(name='person_' + str(no)) for no in range(2)]
        self.countries = [Country.objects.create(name='country_' + str(no)) for no in range(2)]
        self.user = User.objects.create_user(username='test_user', password='test_pwd')

    def test_setup(self):
        self.assertEqual(len(self.genres), 2)
        self.assertEqual(len(self.people), 2)
        self.assertEqual(len(self.countries), 2)

    def test_creating_movie_without_user(self):
        with self.assertRaises(IntegrityError):
            Movie.objects.create(title='test_movie', year=1999)

    def test_creating_movie(self):
        movie = Movie.objects.create(title='title', year=1999, user=self.user)
        self.assertIsInstance(movie, Movie)
        self.assertEqual(movie.imdb_rating, 0.0)
        self.assertEqual(movie.metascore, 0)

    def test_add_m2m_fields(self):
        movie = self._create_movie_with_relations()
        self.assertEqual(movie.genre.count(), 2)
        self.assertEqual(movie.actors.count(), 1)
        self.assertEqual(movie.director.count(), 1)
        self.assertEqual(movie.country.count(), 2)

    def test_relations(self):
        self._create_movie_with_relations()
        genre_count = Genre.objects.all().values('movie').distinct().count()
        director_count = Person.objects.exclude(director=None).distinct().count()
        actor_count = Person.objects.exclude(actors=None).distinct().count()
        country_count = Country.objects.all().values('movie').distinct().count()
        self.assertEqual(genre_count, 1)
        self.assertEqual(director_count, 1)
        self.assertEqual(actor_count, 1)
        self.assertEqual(country_count, 1)

    def _create_movie_with_relations(self):
        movie = Movie.objects.create(title='title', year=1999, user=self.user)
        movie.genre.add(*self.genres)
        movie.actors.add(self.people[0])
        movie.director.add(self.people[1])
        movie.country.add(*self.countries)
        return movie
