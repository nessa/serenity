# -*- coding: utf-8 -*-
from django.forms import widgets
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from recipes.models import Recipe, RecipeCategory, RecipeIngredient
from recipes.models import RecipeDirection, RecipeComment, User
from datetime import datetime

# Users
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


# Recipes
class RecipeCategorySerializer(serializers.ModelSerializer):
    recipe = serializers.CharField(source='recipe.id', read_only=True)

    class Meta:
        model = RecipeCategory
        fields = ('recipe', 'name',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = serializers.CharField(source='recipe.id', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'sort_number', 'quantity', 'name',
            'measurement_unit')


class RecipeDirectionSerializer(serializers.ModelSerializer):
    recipe = serializers.CharField(source='recipe.id', read_only=True)
    image = serializers.URLField(required=False, allow_blank=True)
    video = serializers.URLField(required=False, allow_blank=True)
    time = serializers.FloatField(required=False)

    class Meta:
        model = RecipeDirection
        fields = ('recipe', 'sort_number', 'description', 'image', 'video',
            'time')


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
        fields = ('id', 'title', 'owner', 'language', 'type_of_dish',
            'difficulty', 'created_timestamp', 'updated_timestamp',
            'cooking_time', 'image', 'total_rating', 'users_rating',
            'servings', 'source', 'categories', 'ingredients', 'directions',
            'comments')
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

    # Override update method to update nested fields if needed
    def update(self, instance, validated_data):
        categories = validated_data.pop('categories')
        ingredients = validated_data.pop('ingredients')
        directions = validated_data.pop('directions')

        # Update the recipe instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Delete any categories not included in the request
        category_names = [item['name'] for item in categories]
        for category in instance.categories.all():
            if category.name not in category_names:
                category.delete()

        # Create or update category instances that are in the request
        for item in categories:
            try:
                category = RecipeCategory.objects.get(recipe=instance,
                    name=item['name'])
            except RecipeCategory.DoesNotExist:
                # Create a new category
                category = RecipeCategory(recipe=instance, name=item['name'])
                category.save()

        # Delete any ingredients not included in the request
        ingredient_sort_numbers = [item['sort_number'] for item in ingredients]
        for ingredient in instance.ingredients.all():
            if ingredient.sort_number not in ingredient_sort_numbers:
                 ingredient.delete()

        # Create or update ingredient instances that are in the request
        for item in ingredients:
            try:
                ingredient = RecipeIngredient.objects.get(recipe=instance,
                    sort_number = item['sort_number'])
            except RecipeIngredient.DoesNotExist:
                # Create a new ingredient
                ingredient = RecipeIngredient(recipe=instance,
                    sort_number=item['sort_number'],
                    quantity=item['quantity'],
                    name=item['name'],
                    measurement_unit=item['measurement_unit'])

            # Update present ingredient
            ingredient.quantity = item['quantity']
            ingredient.name = item['name']
            ingredient.measurement_unit = item['measurement_unit']
            ingredient.save()

        # Delete any directions not included in the request
        direction_sort_numbers = [item['sort_number'] for item in directions]
        for direction in instance.directions.all():
            if direction.sort_number not in direction_sort_numbers:
                direction.delete()

        # Create or update direction instances that are in the request
        for item in directions:
            try:
                direction = RecipeDirection.objects.get(recipe=instance,
                    sort_number=item['sort_number'])
            except RecipeDirection.DoesNotExist:
                # Create a new direction
                direction = RecipeDirection(recipe=instance,
                    sort_number=item['sort_number'],
                    description=item['description'],
                    image=item['image'],
                    video=item['video'],
                    time=item['time'])
            
            # Update present direction
            direction.description = item['description']
            direction.image = item['image']
            direction.video = item['video']
            direction.time = item['time']
            direction.save()

        return instance


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     recipes = serializers.HyperlinkedRelatedField(many=True,
#         view_name='recipe-detail', read_only=True)

#     first_name = serializers.CharField(required=False)
#     last_name = serializers.CharField(required=False)
#     auth_token = serializers.CharField(read_only=True)
#     last_login_on = serializers.DateTimeField(source='last_login',
#         read_only=True)
#     joined_on = serializers.DateTimeField(source='date_joined', read_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'email', 'url', 'auth_token', 'first_name',
#             'last_name', 'is_staff', 'last_login_on', 'joined_on',
#             'recipes')
