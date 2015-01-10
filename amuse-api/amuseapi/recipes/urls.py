# -*- coding: utf-8 -*- 
from django.conf.urls import patterns, url
from recipes import views

urlpatterns = [
    url(r'^recipes/$', views.recipe_list),
    url(r'^recipes/(?P<pk>[0-9]+)/$', views.recipe_detail),
]
