# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Search a way to do this programatically
LANGUAGE_CHOICES = (
    ('es', 'Español'),
    ('en', 'English'),
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


CATEGORIES = (
    ('GLUTEN_ALLERGY', 'Not suitable for celiacs'),
    ('LACTOSE_ALLERGY', 'Not suitable for lactose intolerants'),
    ('SHELLFISH_ALLERGY', 'Not suitable for allergics to shellfish'),
    ('FISH_ALLERGY', 'Not suitable for allergics to fish'),
    ('DRIED_FRUIT_ALLERGY', 'Not suitable for allergics to dried fruits'),
    ('VEGETARIAN', 'Vegetarian'),
    ('VEGAN', 'Vegan'),
    ('MEDITERRANEAN', 'Mediterranean'),
)


class User(AbstractUser):
    name = models.CharField(max_length=100, default="")
    surname = models.CharField(max_length=100, default="")
    birthday = models.DateField(blank=True, null=True)
    
# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Recipes with ingredients and directions
class Recipe(models.Model):
    title = models.CharField(max_length=100, blank=False)
    owner = models.ForeignKey(User, related_name='recipes')
    language = models.CharField(choices=LANGUAGE_CHOICES, default='es',
        max_length=10)
    type_of_dish = models.CharField(choices=MENU, default='OTHER',
        max_length=20)
    difficulty = models.CharField(choices=DIFFICULTY, default='MEDIUM',
        max_length=10)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    cooking_time = models.FloatField()
    image = models.URLField(blank=True)
    total_rating = models.IntegerField(default=0)
    users_rating = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    comments_number = models.IntegerField(default=0)
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
