from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^representative/(?P<group_kind>\w+)/(?P<chamber>.+)/(?P<group>.+)/$',
        views.RepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^representative/(?P<group_kind>\w+)/(?P<group>.+)/$',
        views.RepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^representative/(?P<slug>[-\w]+)/$',
        views.RepresentativeDetail.as_view(),
        name='representative-detail'
    ),
    url(
        r'representative/',
        views.RepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^groups/$',
        views.GroupList.as_view(),
        name='group-list'
    ),
    url(
        r'^groups/(?P<kind>\w+)/$',
        views.GroupList.as_view(),
        name='group-list'
    )
]
