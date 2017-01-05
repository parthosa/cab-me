from django.views.generic import RedirectView
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^register/', views.Init_Reg, name='initreg'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name = 'logout'),
    url(r'^verify_otp/', views.verify_otp, name='verify_otp'),
    url(r'^contact/', views.social_profile_build, name='contact')
]