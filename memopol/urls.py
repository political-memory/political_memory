# coding: utf-8

from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from graphene.contrib.django.views import GraphQLView

from memopol_graphene_api.schema import schema

from views.home import HomeView

from views.dossier_ac import ProposalAutocomplete
from views.dossier_detail_base import DossierDetailBase
from views.dossier_detail_recommendations import DossierDetailRecommendations
from views.dossier_detail_proposals import DossierDetailProposals
from views.dossier_detail_documents import DossierDetailDocuments
from views.dossier_list import DossierList

from views.representative_detail_base import RepresentativeDetailBase
from views.representative_detail_votes import RepresentativeDetailVotes
from views.representative_detail_mandates import RepresentativeDetailMandates
from views.representative_detail_positions import RepresentativeDetailPositions
from views.representative_list import RepresentativeList

from views.redirects import (
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

from .legacy_urls import urlpatterns as legacy_patterns

import api


admin.autodiscover()

urlpatterns = [

    # Imported URLs

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(api.router.urls)),

    url(r'^graphql', csrf_exempt(GraphQLView.as_view(schema=schema))),
    url(r'^graphiql', include('django_graphiql.urls')),

    # Homepage

    url(r'^$', HomeView.as_view(), name='home'),

    # Representative list

    url(
        r'^representatives/$',
        RepresentativeList.as_view(),
        name='representative-list'
    ),

    # Representative detail

    url(
        r'^representatives/(?P<slug>[-\w]+)/$',
        RedirectRepresentativeDetail.as_view(),
        name='representative-detail'
    ),

    url(
        r'^representatives/(?P<slug>[-\w]+)/votes/$',
        RepresentativeDetailVotes.as_view(),
        name='representative-votes'
    ),

    url(
        r'^representatives/(?P<slug>[-\w]+)/mandates/$',
        RepresentativeDetailMandates.as_view(),
        name='representative-mandates'
    ),

    url(
        r'^representatives/(?P<slug>[-\w]+)/positions/$',
        RepresentativeDetailPositions.as_view(),
        name='representative-positions'
    ),

    # Dossier list

    url(
        r'^dossiers/$',
        DossierList.as_view(),
        name='dossier-list'
    ),

    # Dossier detail

    url(
        r'^dossiers/(?P<pk>\d+)/$',
        RedirectDossierDetail.as_view(),
        name='dossier-detail'
    ),

    url(
        r'^dossiers/(?P<pk>\d+)/recommendations/$',
        DossierDetailRecommendations.as_view(),
        name='dossier-recommendations'
    ),

    url(
        r'^dossiers/(?P<pk>\d+)/proposals/$',
        DossierDetailProposals.as_view(),
        name='dossier-proposals'
    ),

    url(
        r'^dossiers/(?P<pk>\d+)/documents/$',
        DossierDetailDocuments.as_view(),
        name='dossier-documents'
    ),

    # Dossier autocomplete for admin

    url(
        r'^autocomplete/proposal/$',
        ProposalAutocomplete.as_view(),
        name='proposal-autocomplete',
    ),

    # Theme list

    url(
        r'^themes/$',
        ThemeList.as_view(),
        name='theme-list'
    ),

    # Theme detail

    url(
        r'^themes/(?P<slug>[-\w]+)/$',
        RedirectThemeDetail.as_view(),
        name='theme-detail'
    ),

    url(
        r'^themes/(?P<slug>[-\w]+)/links/$',
        ThemeDetailLinks.as_view(),
        name='theme-links'
    ),

    url(
        r'^themes/(?P<slug>[-\w]+)/dossiers/$',
        ThemeDetailDossiers.as_view(),
        name='theme-dossiers'
    ),

    url(
        r'^themes/(?P<slug>[-\w]+)/proposals/$',
        ThemeDetailProposals.as_view(),
        name='theme-proposals'
    ),

    url(
        r'^themes/(?P<slug>[-\w]+)/positions/$',
        ThemeDetailPositions.as_view(),
        name='theme-positions'
    ),

    # Group URLs

    url(
        r'^groups/(?P<group_kind>[-\w]+)/(?P<group>[^/]+)/$',
        RedirectGroupRepresentativeList.as_view(),
        name='redirect-group-representative-list'
    ),

    # Testing URLs

    url(
        r'^representatives/(?P<slug>[-\w]+)/none/$',
        RepresentativeDetailBase.as_view(),
        name='representative-none'
    ),

    url(
        r'^dossiers/(?P<pk>\d+)/none/$',
        DossierDetailBase.as_view(),
        name='dossier-none'
    ),

    url(
        r'^themes/(?P<slug>[-\w]+)/none/$',
        ThemeDetailBase.as_view(),
        name='theme-none'
    ),

] + legacy_patterns
