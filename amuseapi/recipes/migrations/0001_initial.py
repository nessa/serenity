# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('language', models.CharField(choices=[('ES', 'Español'), ('EN', 'English')], default='ES', max_length=10)),
                ('type_of_dish', models.CharField(choices=[('APPETIZER', 'Appetizer'), ('FIRST-COURSE', 'First Course'), ('SECOND-COURSE', 'Second Course'), ('MAIN-DISH', 'Main Dish'), ('DESSERT', 'Dessert'), ('OTHER', 'Other')], default='OTHER', max_length=20)),
                ('difficulty', models.CharField(choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')], default='MEDIUM', max_length=10)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('cooking_time', models.FloatField()),
                ('image', models.URLField(blank=True)),
                ('total_rating', models.IntegerField()),
                ('users_rating', models.IntegerField()),
                ('servings', models.IntegerField()),
                ('source', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='recipes')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('recipe', models.ForeignKey(to='recipes.Recipe', related_name='categories')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeComment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('comment', models.TextField()),
                ('timestamp', models.DateField(auto_now=True)),
                ('recipe', models.ForeignKey(to='recipes.Recipe', related_name='comments')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeDirection',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('sort_number', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('image', models.URLField(blank=True)),
                ('video', models.URLField(blank=True)),
                ('time', models.FloatField()),
                ('recipe', models.ForeignKey(to='recipes.Recipe', related_name='directions')),
            ],
            options={
                'ordering': ['sort_number'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('sort_number', models.PositiveIntegerField()),
                ('quantity', models.FloatField()),
                ('name', models.CharField(max_length=100)),
                ('measurement_unit', models.CharField(choices=[('g', 'gram'), ('kg', 'kilogram'), ('ml', 'milliliter'), ('l', 'liter'), ('unit', 'unit'), ('cup', 'cup'), ('tsp', 'teaspoon'), ('tbsp', 'tablespoon'), ('rasher', 'rasher')], default='unit', max_length=100)),
                ('recipe', models.ForeignKey(to='recipes.Recipe', related_name='ingredients')),
            ],
            options={
                'ordering': ['sort_number'],
            },
        ),
    ]
