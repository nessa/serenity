# -*- coding: utf-8 -*-
from recipes.models import Recipe, User, RecipeComment, RecipeRating
from django.contrib.auth.models import Group

from rest_framework import viewsets

from recipes.serializers import RecipeSerializer, UserSerializer
from recipes.serializers import RecipeCommentSerializer
from recipes.serializers import RecipeRatingSerializer
from recipes.serializers import GroupSerializer
from rest_framework import generics
from rest_framework import permissions
from recipes.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import detail_route
import rest_framework_filters as filters
from rest_framework.filters import OrderingFilter


from pprint import pprint

## ROOT
@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'recipes': reverse('recipe-list', request=request, format=format)
    })


## USERS
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsOwnerOrReadOnly,)



## RECIPES

# TODO: Add rating filter (using both total_rating and users_rating)
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
    language = filters.CharFilter(name='language', lookup_type='exact')
    type_of_dish = filters.CharFilter(name='type_of_dish',
        lookup_type='exact')
    difficulty = filters.CharFilter(name='difficulty',
        lookup_type='exact')
    
    # Relationships
    categories = filters.CharFilter(name='categories__name',
        lookup_type='contains')
    ingredients = filters.CharFilter(name='ingredients__name',
        lookup_type='contains')
    users = filters.CharFilter(name='users__username',
        lookup_type='contains')

    class Meta:
        model = Recipe
        fields = ['title', 'created_before', 'created_after', 'updated_before',
            'updated_after', 'servings', 'servings_bigger', 'servings_lower',
            'average_rating', 'rating_bigger', 'rating_lower', 'language',
            'type_of_dish', 'difficulty', 'categories', 'ingredients', 'users']


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_class = RecipeFilter
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (OrderingFilter,)
    ordering_fields = '__all__'
    ordering = ('updated_timestamp')
        

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 10


## COMMENTS

class RecipeCommentFilter(filters.FilterSet):
    # Relationships
    recipes = filters.CharFilter(name='recipes__id',
        lookup_type='contains')
    users = filters.CharFilter(name='users__username',
        lookup_type='contains')

    class Meta:
        model = RecipeComment
        fields = ['recipes', 'users']


class RecipeCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = RecipeComment.objects.all()
    serializer_class = RecipeCommentSerializer
    filter_class = RecipeCommentFilter
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 10


## RATINGS

class RecipeRatingFilter(filters.FilterSet):
    # Relationships
    recipes = filters.CharFilter(name='recipes__id',
        lookup_type='contains')
    users = filters.CharFilter(name='users__username',
        lookup_type='contains')

    class Meta:
        model = RecipeRating
        fields = ['recipes', 'users']


class RecipeRatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    queryset = RecipeRating.objects.all()
    serializer_class = RecipeRatingSerializer
    filter_class = RecipeRatingFilter
    #permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        print("PERFORM CREATE")
        pprint(self)
        print(self.request.user)
        serializer.save(owner=self.request.user)

    def get_paginate_by(self):
        """
        Use smaller pagination for HTML representations.
        """
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 10
