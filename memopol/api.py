from rest_framework import routers

from representatives.api import (
    CountryViewSet,
    ChamberViewSet,
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

router.register('countries', CountryViewSet, 'api-country')
router.register('chambers', ChamberViewSet, 'api-chamber')
router.register('constituencies', ConstituencyViewSet, 'api-constituency')
router.register('dossiers', DossierViewSet, 'api-dossier')
router.register('dossier_scores', DossierScoreViewSet, 'api-dossierscore')
router.register('groups', GroupViewSet, 'api-group')
router.register('mandates', MandateViewSet, 'api-mandate')
router.register('proposals', ProposalViewSet, 'api-proposal')
router.register('recommendations', RecommendationViewSet, 'api-recommendation')
router.register('representatives', RepresentativeViewSet, 'api-representative')
router.register('scores', RepresentativeScoreViewSet, 'api-score')
router.register('vote_scores', VoteScoreViewSet, 'api-votescore')
router.register('votes', VoteViewSet, 'api-vote')
