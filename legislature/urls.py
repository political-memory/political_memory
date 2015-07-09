from django.conf.urls import url

from views import representative
from views import group

urlpatterns = [
    # List of groups by group kind
    url(
        r'^groups/(?P<kind>\w+)?$',
        group.index,
        name='group_index'
    ),
    # Representative detail by representative name
    url(
        r'^(?P<name>[-\w]+)$',
        representative.detail,
        name='representative_detail'
    ),
    # Representative detail by representative pk
    url(
        r'^(?P<pk>\d+)$',
        representative.detail,
        name='representative_detail'
    ),
    # List of representatives by group kind and group name or pk
    url(
        r'^(?P<group_kind>\w+)/(?P<group>.+)$',
        representative.index,
        name='representative_index'
    ),
    # List all representatives by default
    url(
        r'',
        representative.index,
        name='representative_index'
    ),
]
