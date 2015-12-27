from django.conf.urls import url

import views

urlpatterns = [
    url(
        r'^dossier/(?P<pk>\d+)/$',
        views.DossierDetail.as_view(),
        name='dossier-detail'
    ),
    url(
        r'dossier/$',
        views.DossierList.as_view(),
        name='dossier-list'
    ),
]
