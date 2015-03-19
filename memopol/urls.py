from django.conf.urls import patterns, include, url
from django.contrib import admin

import core.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'memopol.views.home', name='home'),
    url(r'^$', core.views.HomeView.as_view(), name='index'),
    url('', include('legislature.urls', namespace='legislature')),
    url(r'^admin/', include(admin.site.urls)),
)
