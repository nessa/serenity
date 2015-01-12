# -*- coding: utf-8 -*-
from django.forms import widgets
from rest_framework import serializers
from recipes.models import Recipe, Category, Ingredient, Direction, Comment
from api.users.models import User
from datetime import datetime

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('quantity', 'name', 'measurement_unit')

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ('sort_number', 'description', 'image', 'video', 'time')

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')

    class Meta:
        model = Comment
        fields = ('user', 'comment', 'timestamp')


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(source='owner.email')

    total_rating = serializers.IntegerField(required=False)
    users_rating = serializers.IntegerField(required=False)

    categories = CategorySerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)
    directions = DirectionSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'language', 'created_timestamp', 'updated_timestamp',
                  'cooking_time', 'image', 'total_rating', 'users_rating', 'servings',
                  'source', 'categories', 'ingredients', 'directions', 'comments')
        read_only_fields = ('created_timestamp', 'updated_timestamp')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    recipes = serializers.HyperlinkedRelatedField(many=True, view_name='recipe-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'recipes')
