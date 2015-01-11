# -*- coding: utf-8 -*-
from django.forms import widgets
from rest_framework import serializers
from recipes.models import Recipe, LANGUAGE_CHOICES, MEASUREMENT_CHOICES
from api.users.models import User

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    # ReadOnlyField == CharField(read_only=True)
    owner = serializers.CharField(source='owner.email')
    
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'language', 'created_timestamp', 'updated_timestamp',
                  'cooking_time', 'image', 'total_rating', 'users_rating', 'servings',
                  'source', 'categories', 'ingredients', 'directions', 'comments')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    recipes = serializers.HyperlinkedRelatedField(many=True, view_name='recipe-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'recipes')
