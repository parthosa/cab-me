from django.views.generic import RedirectView
from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^bookcab/', views.bookcab, name='bookcab'),
    url(r'^booknow/', views.booknow, name='booknow'),
    url(r'^postcab/', views.postcab, name = 'postcab'),
    url(r'^main/', views.index, name='index'),
    url(r'^hotels/', views.hotels, name='hotels'),
    url(r'^buses/', views.bus, name='bus'),
    url(r'^flights/', views.flights, name='flights'),
    url(r'^blog/', views.blog, name='blog'),
    url(r'^about/', views.about, name='about'),
    url(r'^routes/', views.routes, name='routes'),
    url(r'^press_release/', views.press_release, name='press_release'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^career/', views.career, name='career'),
    url(r'^feedbacks/', views.feedback, name='feedback'),
    url(r'^privacy_policy/', views.privacy_policy, name='privacy_policy'),
    url(r'^terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    # url(r'^search/', views.search, name='search'),
    url(r'^summary/', views.summary, name='summary'),
    url(r'^cab/cities/', views.cab_cities, name='cab_cities'),
]