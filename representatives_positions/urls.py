from django.conf.urls import url

import views

urlpatterns = [
    url(
        r'^position/create/$',
        views.PositionCreate.as_view(),
        name='position-create'
    ),
    url(
        r'^position/(?P<pk>\d+)/$',
        views.PositionDetail.as_view(),
        name='position-detail'
    ),
]
