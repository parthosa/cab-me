from django.views.generic import RedirectView
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^register_app/$', views.register_app, name='register_app'),
    url(r'^login_app/', views.login_app, name='login_app'),
    url(r'^register/', views.Init_Reg, name='initreg'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name = 'logout'),
    url(r'^verify_otp/', views.verify_otp, name='verify_otp'),
    url(r'^register_success/', views.register_success, name='register_success'),
    url(r'^login_success/', views.login_success, name='login_success'),
    url(r'^social/contact/', views.social_contact, name='social_contact'),
    url(r'^social/facebook/login/', views.social_login_fb, name = 'social_login_fb'),
    url(r'^app/login/', views.user_login_app, name='login'),
    url(r'^app/social/facebook/login/', views.social_login_fb_app, name = 'social_login_fb')
]

