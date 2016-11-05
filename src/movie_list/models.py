from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User)
    description = models.TextField(blank=True, max_length=300)
    metascore = models.IntegerField(blank=True, default=0)
    imdb_rating = models.FloatField(blank=True, default=0.0)
    imdb_url = models.URLField(blank=True, null=True)
    icon = models.URLField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    country = models.ManyToManyField(Country, blank=True)
    director = models.ManyToManyField(Person, blank=True, related_name='director')
    actors = models.ManyToManyField(Person, blank=True, related_name='actors')

    class Meta:
        unique_together = ('title', 'year', 'user')

    def __str__(self):
        return '{title} ({year})'.format(title=self.title, year=self.year)
