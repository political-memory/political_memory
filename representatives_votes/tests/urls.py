from django.conf.urls import include, url

from rest_framework import routers

from representatives_votes.api import (
    DossierViewSet,
    ProposalViewSet,
    VoteViewSet,
)

router = routers.DefaultRouter()
router.register(r'dossiers', DossierViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    url(r'api/', include(router.urls)),
]
