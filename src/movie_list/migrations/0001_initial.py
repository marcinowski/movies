# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-04 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(upload_to='')),
                ('title', models.TextField(max_length=300)),
                ('description', models.TextField(blank=True, max_length=300)),
                ('url', models.URLField(blank=True)),
                ('release_date', models.DateField(blank=True)),
            ],
        ),
    ]