"""amuseapi URL Configuration

The `urlpatterns` list routes URLs to views.
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from recipes import views
from rest_framework.authtoken import views as auth_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'comments', views.RecipeCommentViewSet)
router.register(r'ratings', views.RecipeRatingViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'translations', views.TranslationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
)
