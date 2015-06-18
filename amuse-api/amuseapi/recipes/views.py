# -*- coding: utf-8 -*-
from recipes.models import Recipe, User
from recipes.serializers import RecipeSerializer, UserSerializer
from rest_framework import generics
from rest_framework import permissions
from recipes.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import detail_route
import django_filters


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'recipes': reverse('recipe-list', request=request, format=format)
    })

# TODO: Add a comment list class to create and list them (with filters)

# TODO: Add rating filter (using both total_rating and users_rating)
class RecipeFilter(django_filters.FilterSet):
    created_before = django_filters.DateTimeFilter(name="created_timestamp",
        lookup_type='lt')
    created_after = django_filters.DateTimeFilter(name="created_timestamp",
        lookup_type='ge')
    updated_before = django_filters.DateTimeFilter(name="updated_timestamp",
        lookup_type='lt')
    updated_after = django_filters.DateTimeFilter(name="updated_timestamp",
        lookup_type='ge')
    servings_bigger = django_filters.NumberFilter(name="servings",
        lookup_type = 'ge')   
    servings_lower = django_filters.NumberFilter(name="servings",
        lookup_type = 'le')
    # Exact (or iexact to be case-insensitive)
    language = django_filters.CharFilter(name='language', lookup_type='exact')
    type_of_dish = django_filters.CharFilter(name='type_of_dish',
        lookup_type='exact')
    difficulty = django_filters.CharFilter(name='difficulty',
        lookup_type='exact')
    # Relationships
    categories = django_filters.CharFilter(name='categories__name',
        lookup_type='contains')
    ingredients = django_filters.CharFilter(name='ingredients__name',
        lookup_type='contains')
    users = django_filters.CharFilter(name='users__email',
        lookup_type='contains')

    class Meta:
        model = Recipe
        fields = ['title', 'created_before', 'created_after', 'updated_before',
            'updated_after', 'servings', 'servings_bigger', 'servings_lower',
            'language', 'type_of_dish', 'difficulty', 'categories',
            'ingredients', 'users']


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_class = RecipeFilter
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


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    # TODO: Remove permissions. Restricted to authenticated users, not only
    # owners.
    # rate_recipe method: receives id_recipe (recipe pk) and rating (1 to 5
    # integer)
    #@api_view(['POST'])
    #@permission_classes((IsOwnerOrReadOnly,))
    @detail_route(methods=['post'])#, permission_classes=[IsOwnerOrReadOnly])
    def rate_recipe(self, request, pk=None):
        print("PRUEBA")
        

        if 'rating' in request.POST:
            id_recipe = request.POST['id_recipe']
            rating = request.POST['rating']
            recipe = Recipe.objects.get(pk=pk)

            if recipe:
                self.check_object_permissions(self.request, recipe)

                recipe.total_rating = recipe.total_rating + rating
                recipe.users_rating = recipe.users_rating + 1

                print("Rating:" + recipe.total_rating)
                #recipe.save()

                # TODO: Add new relation between user and rated recipe (future)

                # TODO: Response with the new total_rating and the new
                # users_rating
                return HttpResponse("OK")
            else:
                raise Http404("No recipe")
        else:
            error_format = _('Missing arguments: id recipe and rating')
            raise Http404(error_format)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,)
