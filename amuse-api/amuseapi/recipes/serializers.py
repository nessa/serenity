# -*- coding: utf-8 -*-
from django.forms import widgets
from rest_framework import serializers
from recipes.models import Recipe, LANGUAGE_CHOICES, MEASUREMENT_CHOICES
from api.users.models import User

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        # ReadOnlyField == CharField(read_only=True)
        owner = serializers.CharField(source='owner.username')
        fields = ('id', 'title', 'language', 'created_timestamp', 'updated_timestamp',
                  'cooking_time', 'image', 'total_rating', 'users_rating', 'servings',
                  'source', 'categories', 'ingredients', 'directions', 'comments')

class UserSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(many=True, queryset=Recipe.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'recipes')
