# coding: utf-8
from django.conf.urls import include, patterns, url
from django.contrib import admin

import core.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', core.views.HomeView.as_view(), name='index'),
    url(r'^legislature/', include('legislature.urls',
        namespace='legislature')),
    url(r'^votes/', include('votes.urls', namespace='votes')),
    url(r'^positions/', include('positions.urls', namespace='positions')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
