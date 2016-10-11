# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-11 19:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie_list', '0006_auto_20161011_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='actors',
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(blank=True, null=True, related_name='actors', to='movie_list.Person'),
        ),
        migrations.RemoveField(
            model_name='movie',
            name='country',
        ),
        migrations.AddField(
            model_name='movie',
            name='country',
            field=models.ManyToManyField(blank=True, null=True, to='movie_list.Country'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='director', to='movie_list.Person'),
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(blank=True, null=True, to='movie_list.Genre'),
        ),
    ]
