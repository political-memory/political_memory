# coding: utf-8
from django.conf.urls import url

from views import PositionCreate, PositionDetail

urlpatterns = [
    url(
        r'^create',
        PositionCreate.as_view(),
        name='position-create'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        PositionDetail.as_view(),
        name='position-detail'
    )
]
