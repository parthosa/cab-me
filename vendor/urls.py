from django.views.generic import RedirectView
from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^register/', views.Init_Reg, name='Init_Reg'),
    url(r'^register_success/', views.register_success, name='register_success'),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^login_success/', views.login_success, name='login_success'),
    url(r'^logout/', views.user_logout, name = 'user_logout'),
    url(r'^add_cab/', views.add_cab, name = 'add_cab'),
    url(r'^view_cabs/', views.view_cabs, name = 'view_cabs'),
]