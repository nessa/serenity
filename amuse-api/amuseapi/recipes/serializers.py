# -*- coding: utf-8 -*-
from django.forms import widgets
from rest_framework import serializers
from recipes.models import Recipe, LANGUAGE_CHOICES, MEASUREMENT_CHOICES

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'language', 'created_timestamp', 'updated_timestamp',
                  'cooking_time', 'image', 'total_rating', 'users_rating', 'servings',
                  'source', 'categories', 'ingredients', 'directions', 'comments')
