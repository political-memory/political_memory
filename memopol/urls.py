# coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.views import generic

from views.dossier_ac import DossierAutocomplete, ProposalAutocomplete
from views.dossier_detail import DossierDetail
from views.dossier_list import DossierList
from views.group_ac import GroupAutocomplete
from views.group_list import GroupList
from views.representative_detail import RepresentativeDetail
from views.representative_list import RepresentativeList
from views.redirects import RedirectGroupList, RedirectGroupRepresentativeList
from views.theme_detail import ThemeDetail
from views.theme_list import ThemeList

import api

admin.autodiscover()

urlpatterns = [
    url(
        r'^legislature/representative/(?P<group_kind>\w+)/(?P<chamber>.+)/' +
        r'(?P<group>.+)/$',
        RedirectGroupRepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^legislature/representative/(?P<group_kind>\w+)/(?P<group>.+)/$',
        RepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^legislature/representative/$',
        RepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^legislature/representative/(?P<slug>[-\w]+)/$',
        RepresentativeDetail.as_view(),
        name='representative-detail'
    ),
    url(
        r'^legislature/group/$',
        GroupList.as_view(),
        name='group-list'
    ),
    url(
        r'^legislature/groups/$',
        RedirectGroupList.as_view(),
        name='group-list-redirect'
    ),
    url(
        r'^legislature/group/(?P<kind>\w+)/$',
        GroupList.as_view(),
        name='group-list'
    ),
    url(
        r'^legislature/groups/(?P<kind>\w+)/$',
        RedirectGroupList.as_view(),
        name='group-list-redirect'
    ),
    url(
        r'^legislature/autocomplete/group/$',
        GroupAutocomplete.as_view(),
        name='group-autocomplete',
    ),
    url(
        r'^votes/dossier/$',
        DossierList.as_view(),
        name='dossier-list'
    ),
    url(
        r'^votes/dossier/(?P<pk>\d+)/$',
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
    url(
        r'^theme/$',
        ThemeList.as_view(),
        name='theme-list'
    ),
    url(
        r'^theme/(?P<slug>[-\w]+)/$',
        ThemeDetail.as_view(),
        name='theme-detail'
    ),
    url(
        r'^votes/dossier/(?P<pk>\d+)/$',
        DossierDetail.as_view(),
        name='dossier-detail'
    ),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^positions/', include('representatives_positions.urls',
        namespace='representatives_positions')),
    url(r'^api/', include(api.router.urls)),
    url(r'^$', generic.TemplateView.as_view(template_name='home.html')),
]
