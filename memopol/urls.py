# coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.views import generic

from views.dossier_ac import DossierAutocomplete, ProposalAutocomplete
from views.dossier_detail import DossierDetail
from views.dossier_list import DossierList
from views.group_list import GroupList
from views.representative_detail import RepresentativeDetail
from views.representative_list import RepresentativeList

import api

admin.autodiscover()

urlpatterns = [
    # Project-specific overrides
    url(
        r'^legislature/representatives?/(?P<group_kind>\w+)/(?P<chamber>.+)/' +
        r'(?P<group>.+)/$',
        RepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^legislature/representatives?/(?P<group_kind>\w+)/(?P<group>.+)/$',
        RepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^legislature/representatives?/(?P<slug>[-\w]+)/$',
        RepresentativeDetail.as_view(),
        name='representative-detail'
    ),
    url(
        r'^legislature/groups?/$',
        GroupList.as_view(),
        name='group-list'
    ),
    url(
        r'^legislature/groups?/(?P<kind>\w+)/$',
        GroupList.as_view(),
        name='group-list'
    ),
    url(
        r'^legislature/representatives?/$',
        RepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^votes/dossiers?/$',
        DossierList.as_view(),
        name='dossier-list'
    ),
    url(
        r'^votes/dossiers?/(?P<pk>\d+)/$',
        DossierDetail.as_view(),
        name='dossier-detail'
    ),
    url(
        r'^votes/autocomplete/dossier/$',
        DossierAutocomplete.as_view(),
        name='dossier-autocomplete',
    ),
    url(
        r'^votes/autocomplete/proposal/$',
        ProposalAutocomplete.as_view(),
        name='proposal-autocomplete',
    ),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^positions/', include('representatives_positions.urls',
        namespace='representatives_positions')),
    url(r'^api/', include(api.router.urls)),
    url(r'^$', generic.TemplateView.as_view(template_name='home.html')),
]
