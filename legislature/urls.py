from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        r'^representatives/?$',
        views.representatives_index,
        name='representatives_index'
    ),
    url(
        r'^representatives/view/(?P<num>\d+)$',
        views.representative_view,
        name='representative_view'
    ),
    url(
        r'^representatives/(?P<group_kind>\w+)/(?P<search>.+)/(?P<group_id>\d+)?$',
        views.representatives_by_group,
        name='representatives_by_group'
    ),
    url(
        r'^representatives/(?P<name>.+)$',
        views.representative_by_name,
        name='representative_view_by_name'
    ),
    url(
        r'^groups/(?P<kind>\w+)$',
        views.groups_by_kind,
        name='groups_by_kind'
    )
)
