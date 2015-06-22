# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.utils.timezone
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True, error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='email address', blank=True, max_length=254)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('avatar', models.CharField(blank=True, max_length=20)),
                ('groups', models.ManyToManyField(verbose_name='groups', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', blank=True, related_query_name='user')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', related_name='user_set', help_text='Specific permissions for this user.', to='auth.Permission', blank=True, related_query_name='user')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('language', models.CharField(default='ES', choices=[('ES', 'Español'), ('EN', 'English')], max_length=10)),
                ('type_of_dish', models.CharField(default='OTHER', choices=[('APPETIZER', 'Appetizer'), ('FIRST-COURSE', 'First Course'), ('SECOND-COURSE', 'Second Course'), ('MAIN-DISH', 'Main Dish'), ('DESSERT', 'Dessert'), ('OTHER', 'Other')], max_length=20)),
                ('difficulty', models.CharField(default='MEDIUM', choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')], max_length=10)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('cooking_time', models.FloatField()),
                ('image', models.URLField(blank=True)),
                ('total_rating', models.IntegerField()),
                ('users_rating', models.IntegerField()),
                ('servings', models.IntegerField()),
                ('source', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('recipe', models.ForeignKey(related_name='categories', to='recipes.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('comment', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('recipe', models.ForeignKey(related_name='comments', to='recipes.Recipe')),
                ('user', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeDirection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sort_number', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('image', models.URLField(blank=True)),
                ('video', models.URLField(blank=True)),
                ('time', models.FloatField()),
                ('recipe', models.ForeignKey(related_name='directions', to='recipes.Recipe')),
            ],
            options={
                'ordering': ['sort_number'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sort_number', models.PositiveIntegerField()),
                ('quantity', models.FloatField()),
                ('name', models.CharField(max_length=100)),
                ('measurement_unit', models.CharField(default='unit', choices=[('g', 'gram'), ('kg', 'kilogram'), ('ml', 'milliliter'), ('l', 'liter'), ('unit', 'unit'), ('cup', 'cup'), ('tsp', 'teaspoon'), ('tbsp', 'tablespoon'), ('rasher', 'rasher')], max_length=100)),
                ('recipe', models.ForeignKey(related_name='ingredients', to='recipes.Recipe')),
            ],
            options={
                'ordering': ['sort_number'],
            },
        ),
    ]
