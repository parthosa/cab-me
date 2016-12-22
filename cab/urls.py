from django.views.generic import RedirectView
from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^bookcab/', views.bookcab, name='bookcab'),
    url(r'^booknow/', views.bookcab, name='booknow'),
    url(r'^postcab/', views.postcab, name = 'postcab'),
    url(r'^feedback/', views.feedback, name = 'feedback'),
    url(r'^main/', views.index, name='index'),
    url(r'^hotels/', views.hotels, name='hotels'),
    # url(r'^search/', views.search, name='search'),
    url(r'^summary/', views.summary, name='summary'),
    url(r'^cab/cities/', views.cab_cities, name='cab_cities'),
]