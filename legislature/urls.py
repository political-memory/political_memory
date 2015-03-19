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
        r'^representatives/(?P<mandate_kind>\w+)/(?P<search>.+)$',
        views.representatives_by_mandate,
        name='representatives_by_mandate'
    ),
    url(
        r'^representatives/(?P<name>.+)$',
        views.representative_by_name,
        name='representative_view_by_name'
    ),
    url(
        r'^group/(?P<kind>\w+)$',
        views.group_by_kind,
        name='group_by_kind'
    )
)
