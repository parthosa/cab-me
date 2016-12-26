from django.views.generic import RedirectView
from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^register/', views.Init_Reg, name='initreg'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name = 'logout'),
]