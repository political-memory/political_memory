# coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin

from views.home import HomeView

from views.dossier_ac import DossierAutocomplete, ProposalAutocomplete
from views.dossier_detail_base import DossierDetailBase
from views.dossier_detail_recommendations import DossierDetailRecommendations
from views.dossier_detail_proposals import DossierDetailProposals
from views.dossier_detail_documents import DossierDetailDocuments
from views.dossier_list import DossierList

from views.group_ac import GroupAutocomplete
from views.group_list import GroupList

from views.representative_detail_base import RepresentativeDetailBase
from views.representative_detail_votes import RepresentativeDetailVotes
from views.representative_detail_mandates import RepresentativeDetailMandates
from views.representative_detail_positions import RepresentativeDetailPositions
from views.representative_list import RepresentativeList

from views.redirects import (
    RedirectGroupList,
    RedirectRepresentativeDetail,
    RedirectThemeDetail,
    RedirectGroupRepresentativeList,
    RedirectDossierDetail
)

from views.theme_detail_base import ThemeDetailBase
from views.theme_detail_links import ThemeDetailLinks
from views.theme_detail_dossiers import ThemeDetailDossiers
from views.theme_detail_proposals import ThemeDetailProposals
from views.theme_detail_positions import ThemeDetailPositions
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
        RedirectRepresentativeDetail.as_view(),
        name='representative-detail'
    ),
    # URL used for testing only
    url(
        r'^legislature/representative/(?P<slug>[-\w]+)/none/$',
        RepresentativeDetailBase.as_view(),
        name='representative-none'
    ),
    url(
        r'^legislature/representative/(?P<slug>[-\w]+)/votes/$',
        RepresentativeDetailVotes.as_view(),
        name='representative-votes'
    ),
    url(
        r'^legislature/representative/(?P<slug>[-\w]+)/mandates/$',
        RepresentativeDetailMandates.as_view(),
        name='representative-mandates'
    ),
    url(
        r'^legislature/representative/(?P<slug>[-\w]+)/positions/$',
        RepresentativeDetailPositions.as_view(),
        name='representative-positions'
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
        RedirectDossierDetail.as_view(),
        name='dossier-detail'
    ),
    url(
        r'^votes/dossier/(?P<pk>\d+)/none/$',
        DossierDetailBase.as_view(),
        name='dossier-none'
    ),
    url(
        r'^votes/dossier/(?P<pk>\d+)/recommendations/$',
        DossierDetailRecommendations.as_view(),
        name='dossier-recommendations'
    ),
    url(
        r'^votes/dossier/(?P<pk>\d+)/proposals/$',
        DossierDetailProposals.as_view(),
        name='dossier-proposals'
    ),
    url(
        r'^votes/dossier/(?P<pk>\d+)/documents/$',
        DossierDetailDocuments.as_view(),
        name='dossier-documents'
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
        RedirectThemeDetail.as_view(),
        name='theme-detail'
    ),
    url(
        r'^theme/(?P<slug>[-\w]+)/none/$',
        ThemeDetailBase.as_view(),
        name='theme-none'
    ),
    url(
        r'^theme/(?P<slug>[-\w]+)/links/$',
        ThemeDetailLinks.as_view(),
        name='theme-links'
    ),
    url(
        r'^theme/(?P<slug>[-\w]+)/dossiers/$',
        ThemeDetailDossiers.as_view(),
        name='theme-dossiers'
    ),
    url(
        r'^theme/(?P<slug>[-\w]+)/proposals/$',
        ThemeDetailProposals.as_view(),
        name='theme-proposals'
    ),
    url(
        r'^theme/(?P<slug>[-\w]+)/positions/$',
        ThemeDetailPositions.as_view(),
        name='theme-positions'
    ),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.router.urls)),
    url(r'^$', HomeView.as_view()),
]
