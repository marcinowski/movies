from django.contrib import admin
from movie_list.models import (Movie, Genre, Person, Country)

# Register your models here.
admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)
