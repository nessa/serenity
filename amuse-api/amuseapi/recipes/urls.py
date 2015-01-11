# -*- coding: utf-8 -*- 
from django.conf.urls import patterns, url
from recipes import views

urlpatterns = [
    url(r'^recipes/$', views.RecipeList.as_view()),
    url(r'^recipes/(?P<pk>[0-9]+)/$', views.RecipeDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]
