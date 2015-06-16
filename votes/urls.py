from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        r'^votes/?$',
        views.votes_index,
        name='votes_index'
    ),
)
