from django.views.generic import RedirectView
from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^bookcab/', views.bookcab, name='bookcab'),
    url(r'^main/', views.index, name='index'),
    url(r'^hotels/', views.hotels, name='hotels'),
    url(r'^blog/', views.blog, name='blog'),
    # url(r'^search/', views.search, name='search'),
    url(r'^summary/', views.summary, name='summary'),
    url(r'^cab/cities/', views.cab_cities, name='cab_cities'),
]