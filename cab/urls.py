from django.views.generic import RedirectView
from django.conf.urls import url, include
from django.contrib import admin
from cab.views import *
from refferal import views


urlpatterns = [
    url(r'^bookcab/', bookcab, name='bookcab'),
    url(r'^booknow/', booknow, name='booknow'),
    url(r'^postcab/', postcab, name = 'postcab'),
    url(r'^$', index, name='index'),
    url(r'^hotels/', hotels, name='hotels'),
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^buses/', bus, name='bus'),
    url(r'^flights/', flights, name='flights'),
    url(r'^blog/', blog, name='blog'),
    url(r'^about/', about, name='about'),
    url(r'^routes/', routes, name='routes'),
    url(r'^press_release/', press_release, name='press_release'),
    url(r'^faq/', faq, name='faq'),
    url(r'^career/', career, name='career'),
    url(r'^feedbacks/', feedback, name='feedback'),
    url(r'^privacy_policy/', privacy_policy, name='privacy_policy'),
    url(r'^terms_and_conditions/', terms_and_conditions, name='terms_and_conditions'),
    # url(r'^search/', search, name='search'),
    url(r'^summary/', summary, name='summary'),
    url(r'^cab/cities/', cab_cities, name='cab_cities'),
    url(r'^wallet/', views.wallet, name='wallet'),
    url(r'^forgot_password/', views.forgot_password, name='forgot_password'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^edit_profile/', views.edit_profile, name='edit_profile'),
]