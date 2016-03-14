# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('rating', models.IntegerField()),
                ('recipe', models.ForeignKey(to='recipes.Recipe', related_name='ratings')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='ratings')),
            ],
        ),
    ]
