# -*- coding: utf-8 -*-
from recipes.models import Recipe, User, RecipeComment, RecipeRating
from recipes.models import Ingredient, TranslatedIngredient
from django.contrib.auth.models import Group

from rest_framework import viewsets

from recipes.serializers import RecipeSerializer, UserSerializer
from recipes.serializers import RecipeCommentSerializer
from recipes.serializers import RecipeRatingSerializer
from recipes.serializers import GroupSerializer
from recipes.serializers import IngredientSerializer
from recipes.serializers import TranslatedIngredientSerializer
from recipes.serializers import TranslationSerializer
from rest_framework import generics
from rest_framework import permissions
from recipes.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import detail_route
import rest_framework_filters as filters
from rest_framework.filters import OrderingFilter


## USERS

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ['username']
        
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter

    def get_permissions(self):
        # Open user registration
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated,)
            
        return super(UserViewSet, self).get_permissions()

    

## RECIPES

class RecipeFilter(filters.FilterSet):
    created_before = filters.DateTimeFilter(name="created_timestamp",
        lookup_type='lt')
    created_after = filters.DateTimeFilter(name="created_timestamp",
        lookup_type='ge')
    updated_before = filters.DateTimeFilter(name="updated_timestamp",
        lookup_type='lt')
    updated_after = filters.DateTimeFilter(name="updated_timestamp",
        lookup_type='ge')
    servings_bigger = filters.NumberFilter(name="servings",
        lookup_type = 'ge')   
    servings_lower = filters.NumberFilter(name="servings",
        lookup_expr = 'le')
    rating_bigger = filters.NumberFilter(name="average_rating",
        lookup_type = 'ge')   
    rating_lower = filters.NumberFilter(name="average_rating",
        lookup_expr = 'le')
    
    # Exact (or iexact to be case-insensitive)
    language = filters.CharFilter(name='language',
        lookup_type='iexact')
    type_of_dish = filters.CharFilter(name='type_of_dish',
        lookup_type='exact')
    difficulty = filters.CharFilter(name='difficulty',
        lookup_type='exact')
    
    # Relationships
    category = filters.CharFilter(name='categories__name',
        lookup_type='contains')
    ingredient = filters.CharFilter(name='ingredients__name',
        lookup_type='contains')
    user = filters.CharFilter(name='owner__username',
        lookup_type='contains')

    class Meta:
        model = Recipe
        fields = ['title', 'created_before', 'created_after', 'updated_before',
            'updated_after', 'servings', 'servings_bigger', 'servings_lower',
            'average_rating', 'rating_bigger', 'rating_lower', 'language',
            'type_of_dish', 'difficulty', 'category', 'ingredient', 'user']


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_class = RecipeFilter
    ordering_filter = OrderingFilter()
    ordering_fields = '__all__'
    ordering = ('updated_timestamp')

    def filter_queryset(self, queryset):
        queryset = super(RecipeViewSet, self).filter_queryset(queryset)
        return self.ordering_filter.filter_queryset(self.request, queryset, self)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 10
    
    def get_permissions(self):
        # Open recipes read
        if self.request.method in SAFE_METHODS:
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsOwnerOrReadOnly,)
            
        return super(RecipeViewSet, self).get_permissions()


## COMMENTS

class RecipeCommentFilter(filters.FilterSet):
    # Relationships
    recipe = filters.CharFilter(name='recipe__id',
        lookup_type='contains')
    user = filters.CharFilter(name='user__username',
        lookup_type='contains')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    class Meta:
        model = RecipeComment
        fields = ['recipe', 'user']


class RecipeCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = RecipeComment.objects.all()
    serializer_class = RecipeCommentSerializer
    filter_class = RecipeCommentFilter
    ordering_filter = OrderingFilter()
    ordering_fields = '__all__'
    ordering = ('-timestamp')

    def filter_queryset(self, queryset):
        queryset = super(RecipeCommentViewSet, self).filter_queryset(queryset)
        return self.ordering_filter.filter_queryset(self.request, queryset, self)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 10

    def get_permissions(self):
        # Open recipes read
        if self.request.method in SAFE_METHODS:
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticatedOrReadOnly,)
            
        return super(RecipeCommentViewSet, self).get_permissions()


## RATINGS

class RecipeRatingFilter(filters.FilterSet):
    # Relationships
    recipe = filters.CharFilter(name='recipe__id',
        lookup_type='contains')
    user = filters.CharFilter(name='user__username',
        lookup_type='contains')

    class Meta:
        model = RecipeRating
        fields = ['recipe', 'user']


class RecipeRatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = RecipeRating.objects.all()
    serializer_class = RecipeRatingSerializer
    filter_class = RecipeRatingFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 10

    def get_permissions(self):
        # Open recipes read
        if self.request.method in SAFE_METHODS:
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticatedOrReadOnly,)
            
        return super(RecipeRatingViewSet, self).get_permissions()


# GENERIC INGREDIENTS
class IngredientFilter(filters.FilterSet):
    class Meta:
        model = Ingredient
        fields = ['code']
        
class TranslationFilter(filters.FilterSet):
    updated_before = filters.DateTimeFilter(name="timestamp", lookup_type='lt')
    updated_after = filters.DateTimeFilter(name="timestamp", lookup_type='ge')
    
    # Exact (or iexact to be case-insensitive)
    language = filters.CharFilter(name='language', lookup_type='iexact')

    class Meta:
        model = TranslatedIngredient
        fields = ['updated_before', 'updated_after', 'language']

        
class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows generic ingredients to be viewed or edited.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_class = IngredientFilter
    ordering_filter = OrderingFilter()
    ordering_fields = '__all__'
    ordering = ('code')

    def filter_queryset(self, queryset):
        queryset = super(IngredientViewSet, self).filter_queryset(queryset)
        return self.ordering_filter.filter_queryset(self.request, queryset, self)

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 10
    
    def get_permissions(self):
        # Open recipes read
        if self.request.method in SAFE_METHODS:
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated,)
            
        return super(IngredientViewSet, self).get_permissions()


class TranslationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows generic ingredients to be viewed or edited.
    """
    queryset = TranslatedIngredient.objects.all()
    serializer_class = TranslationSerializer
    filter_class = TranslationFilter
    ordering_filter = OrderingFilter()
    ordering_fields = '__all__'
    ordering = ('timestamp')

    def filter_queryset(self, queryset):
        queryset = super(TranslationViewSet, self).filter_queryset(queryset)
        return self.ordering_filter.filter_queryset(self.request, queryset, self)

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 10
    
    def get_permissions(self):
        # Open recipes read
        if self.request.method in SAFE_METHODS:
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated,)
            
        return super(TranslationViewSet, self).get_permissions()
