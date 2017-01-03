from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cabme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls', namespace='registration')),
    url(r'^', include('cab.urls', namespace='cab')),
    url(r'^vendor/', include('vendor.urls', namespace='vendor')),
    url(r'^accounts/social/', include('allauth.urls')),
     url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT, })
)
