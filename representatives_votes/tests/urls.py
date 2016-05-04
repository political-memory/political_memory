from django.conf.urls import include, url

from rest_framework import routers

from representatives_votes.api import (
    DossierViewSet,
    ProposalViewSet,
    VoteViewSet,
)

from representatives.api import (
    ConstituencyViewSet,
    GroupViewSet,
    MandateViewSet,
    RepresentativeViewSet,
)

router = routers.DefaultRouter()
router.register(r'constituencies', ConstituencyViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'mandates', MandateViewSet)
router.register(r'representatives', RepresentativeViewSet)
router.register(r'dossiers', DossierViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    url(r'api/', include(router.urls)),
]
