# -*- coding: utf-8 -*-
from django.forms import widgets
from rest_framework import serializers
from recipes.models import Recipe, RecipeCategory, RecipeIngredient
from recipes.models import RecipeDirection, RecipeComment, User
from datetime import datetime


class RecipeCategorySerializer(serializers.ModelSerializer):
    recipe = serializers.CharField(source='recipe.id', read_only=True)

    class Meta:
        model = RecipeCategory
        fields = ('recipe', 'name',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = serializers.CharField(source='recipe.id', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'quantity', 'name', 'measurement_unit')


class RecipeDirectionSerializer(serializers.ModelSerializer):
    recipe = serializers.CharField(source='recipe.id', read_only=True)
    image = serializers.URLField(required=False, allow_blank=True)
    video = serializers.URLField(required=False, allow_blank=True)
    time = serializers.FloatField(required=False)

    class Meta:
        model = RecipeDirection
        fields = ('recipe', 'sort_number', 'description', 'image', 'video', 'time')


class RecipeCommentSerializer(serializers.ModelSerializer):
    recipe = serializers.CharField(source='recipe.id', read_only=True)
    user = serializers.CharField(source='user.id', read_only=True)

    class Meta:
        model = RecipeComment
        fields = ('recipe',  'user', 'comment', 'timestamp')


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(source='owner.id', read_only=True)    
    image = serializers.URLField(required=False, allow_blank=True)
    total_rating = serializers.IntegerField(required=False)
    users_rating = serializers.IntegerField(required=False)

    categories = RecipeCategorySerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True)
    directions = RecipeDirectionSerializer(many=True)
    # Comments will be added in its own method
    comments = RecipeCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'owner', 'language', 'created_timestamp',
                  'updated_timestamp', 'cooking_time', 'image', 'total_rating',
                  'users_rating', 'servings', 'source', 'categories',
                  'ingredients', 'directions', 'comments')
        read_only_fields = ('created_timestamp', 'updated_timestamp',
                            'comments')

    # Override create method to create all nested fields
    def create(self, validated_data):
        categories = validated_data.pop('categories')
        ingredients = validated_data.pop('ingredients')
        directions = validated_data.pop('directions')

        recipe = Recipe.objects.create(**validated_data)

        for category in categories:
            RecipeCategory.objects.create(recipe=recipe, **category)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient)
        for direction in directions:
            RecipeDirection.objects.create(recipe=recipe, **direction)
            
        return recipe

class UserSerializer(serializers.HyperlinkedModelSerializer):
    recipes = serializers.HyperlinkedRelatedField(many=True, view_name='recipe-detail', read_only=True)

    first_name = serializers.CharField(source='first_name', required=False)
    last_name = serializers.CharField(source='last_name', required=False)
    auth_token = serializers.CharField(read_only=True)
    last_login_on = serializers.DateTimeField(source='last_login',
                                              read_only=True)
    joined_on = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'url', 'auth_token', 'first_name',
                  'last_name', 'is_staff', 'last_login_on',
                  'joined_on', 'recipes')
