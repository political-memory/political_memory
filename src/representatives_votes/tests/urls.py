from django.conf.urls import include, url

from rest_framework import routers

from representatives_votes.api import (
    DossierViewSet,
    ProposalViewSet,
    VoteViewSet,
)

from representatives.api import (
    ChamberViewSet,
    ConstituencyViewSet,
    CountryViewSet,
    GroupViewSet,
    MandateViewSet,
    RepresentativeViewSet,
)

router = routers.DefaultRouter()
router.register('countries', CountryViewSet, 'api-country')
router.register('chambers', ChamberViewSet, 'api-chamber')
router.register('constituencies', ConstituencyViewSet, 'api-constituency')
router.register('groups', GroupViewSet, 'api-group')
router.register('mandates', MandateViewSet, 'api-mandate')
router.register('representatives', RepresentativeViewSet, 'api-representative')
router.register('dossiers', DossierViewSet, 'api-dossier')
router.register('proposals', ProposalViewSet, 'api-proposal')
router.register('votes', VoteViewSet, 'api-vote')

urlpatterns = [
    url('api/', include(router.urls)),
]
