# -*- coding: utf-8 -*-
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from rest_framework import generics
from api.users.models import User
from recipes.serializers import UserSerializer
from rest_framework import permissions
from recipes.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
import django_filters


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'recipes': reverse('recipe-list', request=request, format=format)
    })


# TODO: Add rating filter (using both total_rating and users_rating)
class RecipeFilter(django_filters.FilterSet):
    created_before = django_filters.DateTimeFilter(name="created_timestamp", lookup_type='lt')
    created_after = django_filters.DateTimeFilter(name="created_timestamp", lookup_type='ge')
    updated_before = django_filters.DateTimeFilter(name="updated_timestamp", lookup_type='lt')
    updated_after = django_filters.DateTimeFilter(name="updated_timestamp", lookup_type='ge')
    servings_bigger = django_filters.NumberFilter(name="servings", lookup_type = 'ge')   
    servings_lower = django_filters.NumberFilter(name="servings", lookup_type = 'le')
    categories = django_filters.CharFilter(name='categories__name', lookup_type='contains')
    ingredients = django_filters.CharFilter(name='ingredients__name', lookup_type='contains')
    users = django_filters.CharFilter(name='users__email', lookup_type='contains')

    class Meta:
        model = Recipe
        fields = ['title', 'created_before', 'created_after', 'updated_before',
                  'updated_after', 'servings', 'servings_bigger', 'servings_lower',
                  'categories', 'ingredients', 'users']


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_class = RecipeFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    # TODO: Remove permissions. Restricted to authenticated users, not only owners.
    # rate_recipe method: receives id_recipe (recipe pk) and rating (1 to 5 integer)
    def rate_recipe(self, request):
        if request.method == 'POST':
            if 'id_recipe' in request.POST and 'rating' in request.POST:
                id_recipe = request.POST['id_recipe']
                rating = request.POST['rating']
                recipe = Recipe.objects.get(pk=id_recipe)
                if recipe:
                    recipe.total_rating = recipe.total_rating + rating
                    recipe.users_rating = recipe.users_rating + 1
                    recipe.save()

                    # TODO: Add new relation between user and rated recipe (future)

                    # TODO: Response with the new total_rating and the new users_rating
                    return HttpResponse("OK")
                else:
                    raise Http404("No recipe")
            else:
                error_format = _('Missing arguments: id recipe and rating')
                raise Http404(error_format)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
