# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-11 18:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie_list', '0002_auto_20161004_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(default='Comedy', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='url',
            new_name='imdb_url',
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='movie',
            name='language',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='movie',
            name='metascore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='runtime',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.IntegerField(blank=True, default=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(blank=True, default=datetime.date(2016, 10, 10)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actors', to='movie_list.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movie_list.Country'),
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='director', to='movie_list.Person', unique=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, default='', on_delete=django.db.models.deletion.CASCADE, to='movie_list.Genre'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='movie',
            unique_together=set([('title', 'year')]),
        ),
    ]
