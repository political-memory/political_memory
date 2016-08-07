from rest_framework import routers

from rql_filter.backend import RQLFilterBackend as RQLBackend

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


class RQLDossierViewSet(DossierViewSet):
    filter_backends = DossierViewSet.filter_backends + (RQLBackend,)


class RQLProposalViewSet(ProposalViewSet):
    filter_backends = ProposalViewSet.filter_backends + (RQLBackend,)


class RQLVoteViewSet(VoteViewSet):
    filter_backends = VoteViewSet.filter_backends + (RQLBackend,)


router = routers.DefaultRouter()

router.register('countries', CountryViewSet, 'api-country')
router.register('chambers', ChamberViewSet, 'api-chamber')
router.register('constituencies', ConstituencyViewSet, 'api-constituency')
router.register('dossiers', RQLDossierViewSet, 'api-dossier')
router.register('dossier_scores', DossierScoreViewSet, 'api-dossierscore')
router.register('groups', GroupViewSet, 'api-group')
router.register('mandates', MandateViewSet, 'api-mandate')
router.register('proposals', RQLProposalViewSet, 'api-proposal')
router.register('recommendations', RecommendationViewSet, 'api-recommendation')
router.register('representatives', RepresentativeViewSet,
                'api-representative')
router.register('scores', RepresentativeScoreViewSet, 'api-score')
router.register('vote_scores', VoteScoreViewSet, 'api-votescore')
router.register('votes', RQLVoteViewSet, 'api-vote')
