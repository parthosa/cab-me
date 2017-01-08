from django.views.generic import RedirectView
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^invite/?P<invite_code>[\w\-]+)/$', views.refer_registeration, name='refer_registeration'),
    url(r'^get_invite_url/$', views.create_invite_code, name='create_invite_code'),
    url(r'^verify_otp/$', views.verify_otp, name='verify_otp'),
    url(r'^contact/', views.social_profile_build, name='contact')
]