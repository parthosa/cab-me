from django.views.generic import RedirectView
from django.http import HttpResponseRedirect,Http404,HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^invite/(?P<invite_code>[\w\-]+)/$', views.refer_registration, name='refer_registration'),
    url(r'^earn_money/$', views.create_invite_code, name='create_invite_code'),
    url(r'^verify_otp/$', views.verify_otp, name='verify_otp'),
    url(r'^wallet/$', views.wallet, name='wallet'),
    url(r'^contact/', views.social_contact, name='contact')
]