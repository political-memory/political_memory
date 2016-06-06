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

router.register(r'constituencies', ConstituencyViewSet, 'api-constituency')
router.register(r'dossiers', DossierViewSet, 'api-dossier')
router.register(r'dossier_scores', DossierScoreViewSet, 'api-dossierscore')
router.register(r'groups', GroupViewSet, 'api-group')
router.register(r'mandates', MandateViewSet, 'api-mandate')
router.register(r'proposals', ProposalViewSet, 'api-proposal')
router.register(r'recommendations', RecommendationViewSet,
    'api-recommendation')
router.register(r'representatives', RepresentativeViewSet,
    'api-representative')
router.register(r'scores', RepresentativeScoreViewSet, 'api-score')
router.register(r'vote_scores', VoteScoreViewSet, 'api-votescore')
router.register(r'votes', VoteViewSet, 'api-vote')
