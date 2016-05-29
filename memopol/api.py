from rest_framework import routers

from representatives.api import (
    ConstituencyViewSet,
    GroupViewSet,
    MandateViewSet,
    RepresentativeViewSet,
)

from representatives_votes.api import (
    DossierViewSet,
    ProposalViewSet,
    VoteViewSet,
)

from representatives_recommendations.api import (
    DossierScoreViewSet,
    RecommendationViewSet,
    RepresentativeScoreViewSet,
    VoteScoreViewSet
)


router = routers.DefaultRouter()

router.register(r'constituencies', ConstituencyViewSet)
router.register(r'dossiers', DossierViewSet)
router.register(r'dossier_scores', DossierScoreViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'mandates', MandateViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'representatives', RepresentativeViewSet)
router.register(r'scores', RepresentativeScoreViewSet)
router.register(r'vote_scores', VoteScoreViewSet)
router.register(r'votes', VoteViewSet)
