# -*- coding: utf-8 -*-
from django.db import models

# Search a way to do this programatically
LANGUAGE_CHOICES = (
    ('ES', 'Español'),
    ('EN', 'English'),
)

MEASUREMENT_CHOICES = (
    ('g', 'gram'),
    ('kg', 'kilogram'),
    ('unit', 'unit'),
)



class Category(models.Model):
    name = models.CharField(max_length=100)

class Ingredient(models.Model):
    quantity = models.FloatField()
    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(choices=MEASUREMENT_CHOICES, default='unit', max_length=100)

class Direction(models.Model):
    sort_number = models.PositiveIntegerField()
    

class Comment(models.Model):
    # TODO: Add user field properly
    #user = models.ForeignKey('users.User', related_name='comments')
    comment = models.TextField()


# Recipes with ingredientes and directions
class Recipe(models.Model):
    title = models.CharField(max_length=100, blank=False)
    owner = models.ForeignKey('users.User', related_name='recipes')
    language = models.CharField(choices=LANGUAGE_CHOICES, default='ES', max_length=10)
    created_timestamp = models.DateTimeField()
    updated_timestamp = models.DateTimeField(auto_now_add=True)
    cooking_time = models.FloatField()
    image = models.URLField()
    total_rating = models.IntegerField()
    users_rating = models.IntegerField()
    servings = models.IntegerField()
    source = models.CharField(max_length=200)
    
    categories = models.ManyToManyField(Category, verbose_name='list of categories')
    ingredients = models.ManyToManyField(Ingredient, verbose_name='list of ingredients')
    directions = models.ManyToManyField(Direction, verbose_name='list of directions')
    comments = models.ManyToManyField(Comment, verbose_name='list of comments')
