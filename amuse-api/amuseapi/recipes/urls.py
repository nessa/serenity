# -*- coding: utf-8 -*- 
from django.conf.urls import patterns, url
from recipes import views

# API endpoints
urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^recipes/$',
        views.RecipeList.as_view(),
        name='recipe-list'),
    url(r'^recipes/(?P<pk>[0-9]+)/$',
        views.RecipeDetail.as_view(),
        name='recipe-detail'),
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail')
]
