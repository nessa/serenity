# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, verbose_name='username', error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=100, default='')),
                ('surname', models.CharField(max_length=100, default='')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('groups', models.ManyToManyField(to='auth.Group', related_query_name='user', related_name='user_set', blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', related_query_name='user', related_name='user_set', blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=10, choices=[('es', 'Español'), ('en', 'English')], default='es')),
                ('type_of_dish', models.CharField(max_length=20, choices=[('APPETIZER', 'Appetizer'), ('FIRST-COURSE', 'First Course'), ('SECOND-COURSE', 'Second Course'), ('MAIN-DISH', 'Main Dish'), ('DESSERT', 'Dessert'), ('OTHER', 'Other')], default='OTHER')),
                ('difficulty', models.CharField(max_length=10, choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')], default='MEDIUM')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('cooking_time', models.FloatField()),
                ('image', models.URLField(blank=True)),
                ('total_rating', models.IntegerField(default=0)),
                ('users_rating', models.IntegerField(default=0)),
                ('average_rating', models.FloatField(default=0)),
                ('comments_number', models.IntegerField(default=0)),
                ('servings', models.IntegerField()),
                ('source', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('recipe', models.ForeignKey(related_name='categories', to='recipes.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeComment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('comment', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('recipe', models.ForeignKey(related_name='comments', to='recipes.Recipe')),
                ('user', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeDirection',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('sort_number', models.PositiveIntegerField()),
                ('quantity', models.FloatField()),
                ('name', models.CharField(max_length=100)),
                ('measurement_unit', models.CharField(max_length=100, choices=[('g', 'gram'), ('kg', 'kilogram'), ('ml', 'milliliter'), ('l', 'liter'), ('unit', 'unit'), ('cup', 'cup'), ('tsp', 'teaspoon'), ('tbsp', 'tablespoon'), ('rasher', 'rasher')], default='unit')),
                ('recipe', models.ForeignKey(related_name='ingredients', to='recipes.Recipe')),
            ],
            options={
                'ordering': ['sort_number'],
            },
        ),
        migrations.CreateModel(
            name='RecipeRating',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('rating', models.IntegerField()),
                ('recipe', models.ForeignKey(related_name='ratings', to='recipes.Recipe')),
                ('user', models.ForeignKey(related_name='ratings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
