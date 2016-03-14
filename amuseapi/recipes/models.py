# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser

# Search a way to do this programatically
LANGUAGE_CHOICES = (
    ('ES', 'Español'),
    ('EN', 'English'),
)

MEASUREMENT_CHOICES = (
    ('g', 'gram'),
    ('kg', 'kilogram'),
    ('ml', 'milliliter'),
    ('l', 'liter'),
    ('unit', 'unit'),
    ('cup', 'cup'),
    ('tsp', 'teaspoon'),
    ('tbsp', 'tablespoon'),
    ('rasher', 'rasher'),
)

MENU = (
    ('APPETIZER', 'Appetizer'),
    ('FIRST-COURSE', 'First Course'),
    ('SECOND-COURSE', 'Second Course'),
    ('MAIN-DISH', 'Main Dish'),
    ('DESSERT', 'Dessert'),
    ('OTHER', 'Other'),
)

DIFFICULTY = (
    ('HIGH', 'High'),
    ('MEDIUM', 'Medium'),
    ('LOW', 'Low'),
)

# For now
CATEGORIES = (
    ('SUITABLE-FOR-CELIACS', 'Suitable for celiacs'),
    ('SUITABLE-FOR-LACTOSE-INTOLERANTS', 'Suitable for lactose intolerants'),
    ('VEGETARIAN', 'Vegetarian'),
    ('VEGAN', 'Vegan'),
    ('ARAB', 'Arab'),
    ('MEDITERRANEAN', 'Mediterranean'),
    ('ASIAN', 'Asian'),
    ('NORTH-AMERICAN', 'North American'),
    ('SOUTH-AMERICAN', 'South American'),
    ('CENTRAL-AMERICAN', 'Central American'),
    ('AFRICAN', 'African'),
    ('EUROPEAN', 'European'),
    ('OCEANIAN', 'Oceanian'),
)

class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    avatar = models.CharField(max_length=20, blank=True)


# Recipes with ingredients and directions
class Recipe(models.Model):
    title = models.CharField(max_length=100, blank=False)
    owner = models.ForeignKey(User, related_name='recipes')
    language = models.CharField(choices=LANGUAGE_CHOICES, default='ES',
        max_length=10)
    type_of_dish = models.CharField(choices=MENU, default='OTHER',
        max_length=20)
    difficulty = models.CharField(choices=DIFFICULTY, default='MEDIUM',
        max_length=10)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    cooking_time = models.FloatField()
    image = models.URLField(blank=True)
    total_rating = models.IntegerField()
    users_rating = models.IntegerField()
    servings = models.IntegerField()
    source = models.CharField(max_length=200)

class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='categories')
    name = models.CharField(max_length=100)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients')
    sort_number = models.PositiveIntegerField()
    quantity = models.FloatField()
    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(choices=MEASUREMENT_CHOICES,
        default='unit', max_length=100)

    class Meta:
        ordering = ['sort_number']

class RecipeDirection(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='directions')
    sort_number = models.PositiveIntegerField()
    description = models.TextField()
    image = models.URLField(blank=True)
    video = models.URLField(blank=True)
    time = models.FloatField()

    class Meta:
        ordering = ['sort_number']

class RecipeComment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments')
    user = models.ForeignKey(User, related_name='comments')
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

class RecipeRating(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ratings')
    user = models.ForeignKey(User, related_name='ratings')
    rating = models.IntegerField()
