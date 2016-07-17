# -*- coding: utf-8 -*-
from rest_framework import viewsets

# Import models
from recipes.models import Recipe, User, RecipeComment, RecipeRating
from recipes.models import Ingredient, TranslatedIngredient
from django.contrib.auth.models import Group

# Import serializers
from recipes.serializers import RecipeSerializer
from recipes.serializers import UserSerializer, GroupSerializer
from recipes.serializers import RecipeCommentSerializer
from recipes.serializers import RecipeRatingSerializer
from recipes.serializers import GroupSerializer
from recipes.serializers import IngredientSerializer
from recipes.serializers import TranslatedIngredientSerializer
from recipes.serializers import TranslationSerializer

# Import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from recipes.permissions import IsModerator
from recipes.permissions import IsOwnerOrModerator

# Import filters
import rest_framework_filters as filters
from rest_framework.filters import OrderingFilter

# Import pagination classes
from recipes.pagination import LargeResultsSetPagination
from recipes.pagination import StandardResultsSetPagination


# Actions:
# ModelViewSet automatically provides `list`, `create`, `retrieve`,
# `update` and `destroy` actions.


## USERS

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ['username']
        
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    # PERMISSIONS:
    # This endpoint will be completely open only for Moderators.
    # The other users only could see or edit its own user data.
    # The authenticated or unauthenticated users could create new users.

    queryset = User.objects.all()
    filter_class = UserFilter
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination

    def get_permissions(self):
        self.permission_classes = (IsModerator,)
        return super(UserViewSet, self).get_permissions()


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    # PERMISSIONS:
    # This endpoint will be open only for Moderators.

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsModerator,)

    

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

    # PERMISSIONS:
    # This endpoint will be completely open only for Moderators.
    # Only authenticated users and Moderators could create a new recipe.
    # The authenticated or unauthenticated users could see all the recipes.

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LargeResultsSetPagination
    filter_class = RecipeFilter
    ordering_filter = OrderingFilter()
    ordering_fields = '__all__'
    ordering = ('updated_timestamp')


    def get_permissions(self):
        # List and retrieve are open to any user
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = (AllowAny,)
        # Create are open to authenticated users
        elif self.action == 'create':
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsOwnerOrModerator,)
            
        return super(RecipeViewSet, self).get_permissions()


    def filter_queryset(self, queryset):
        queryset = super(RecipeViewSet, self).filter_queryset(queryset)
        return self.ordering_filter.filter_queryset(self.request, queryset, self)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)





## COMMENTS

class RecipeCommentFilter(filters.FilterSet):
    recipe = filters.CharFilter(name='recipe__id',
        lookup_type='contains')
    user = filters.CharFilter(name='user__username',
        lookup_type='contains')

    class Meta:
        model = RecipeComment
        fields = ['recipe', 'user']


class RecipeCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """

    # PERMISSIONS:
    # This endpoint will be completely open for authenticated users.
    # The authenticated or unauthenticated users could see all the comments.

    queryset = RecipeComment.objects.all()
    serializer_class = RecipeCommentSerializer
    pagination_class = StandardResultsSetPagination
    filter_class = RecipeCommentFilter
    ordering_filter = OrderingFilter()
    ordering_fields = '__all__'
    ordering = ('-timestamp')

    def get_permissions(self):
        # Open comments read
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticatedOrReadOnly,)
            
        return super(RecipeCommentViewSet, self).get_permissions()

    def filter_queryset(self, queryset):
        queryset = super(RecipeCommentViewSet, self).filter_queryset(queryset)
        return self.ordering_filter.filter_queryset(self.request, queryset, self)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



## RATINGS

class RecipeRatingFilter(filters.FilterSet):
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

    # PERMISSIONS:
    # This endpoint will be completely open for authenticated users.
    # The authenticated or unauthenticated users could see all the comments.

    queryset = RecipeRating.objects.all()
    serializer_class = RecipeRatingSerializer
    pagination_class = StandardResultsSetPagination
    filter_class = RecipeRatingFilter

    def get_permissions(self):
        # Open ratings read
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticatedOrReadOnly,)
            
        return super(RecipeRatingViewSet, self).get_permissions()


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



## GENERIC INGREDIENTS

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

    # PERMISSIONS:
    # This endpoint will be completely open only for Moderators.

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = StandardResultsSetPagination
    filter_class = IngredientFilter
    ordering_filter = OrderingFilter()
    ordering_fields = '__all__'
    ordering = ('code')


    def get_permissions(self):
        self.permission_classes = (IsModerator,)
        return super(IngredientViewSet, self).get_permissions()


    def filter_queryset(self, queryset):
        queryset = super(IngredientViewSet, self).filter_queryset(queryset)
        return self.ordering_filter.filter_queryset(self.request, queryset, self)



class TranslationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows generic ingredients to be viewed or edited.
    """

    # PERMISSIONS:
    # This endpoint will be completely open only for Moderators.
    # The authenticated or unauthenticated users could see all the translations.

    queryset = TranslatedIngredient.objects.all()
    serializer_class = TranslationSerializer
    pagination_class = LargeResultsSetPagination
    filter_class = TranslationFilter
    ordering_filter = OrderingFilter()
    ordering_fields = '__all__'
    ordering = ('timestamp')


    def get_permissions(self):
        # Open translations read
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsModerator,)
            
        return super(TranslationViewSet, self).get_permissions()


    def filter_queryset(self, queryset):
        queryset = super(TranslationViewSet, self).filter_queryset(queryset)
        return self.ordering_filter.filter_queryset(self.request, queryset, self)

