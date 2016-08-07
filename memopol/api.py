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


class RQLCountryViewSet(CountryViewSet):
    filter_backends = CountryViewSet.filter_backends + [RQLBackend]


class RQLChamberViewSet(ChamberViewSet):
    filter_backends = ChamberViewSet.filter_backends + [RQLBackend]


class RQLConstituencyViewSet(ConstituencyViewSet):
    filter_backends = ConstituencyViewSet.filter_backends + [RQLBackend]


class RQLGroupViewSet(GroupViewSet):
    filter_backends = GroupViewSet.filter_backends + [RQLBackend]


class RQLMandateViewSet(MandateViewSet):
    filter_backends = MandateViewSet.filter_backends + (RQLBackend,)


class RQLRepresentativeViewSet(RepresentativeViewSet):
    filter_backends = RepresentativeViewSet.filter_backends + (RQLBackend,)


class RQLDossierViewSet(DossierViewSet):
    filter_backends = DossierViewSet.filter_backends + (RQLBackend,)


class RQLProposalViewSet(ProposalViewSet):
    filter_backends = ProposalViewSet.filter_backends + (RQLBackend,)


class RQLVoteViewSet(VoteViewSet):
    filter_backends = VoteViewSet.filter_backends + (RQLBackend,)


router = routers.DefaultRouter()

router.register('countries', RQLCountryViewSet, 'api-country')
router.register('chambers', RQLChamberViewSet, 'api-chamber')
router.register('constituencies', RQLConstituencyViewSet, 'api-constituency')
router.register('dossiers', RQLDossierViewSet, 'api-dossier')
router.register('dossier_scores', DossierScoreViewSet, 'api-dossierscore')
router.register('groups', RQLGroupViewSet, 'api-group')
router.register('mandates', RQLMandateViewSet, 'api-mandate')
router.register('proposals', RQLProposalViewSet, 'api-proposal')
router.register('recommendations', RecommendationViewSet, 'api-recommendation')
router.register('representatives', RQLRepresentativeViewSet,
                'api-representative')
router.register('scores', RepresentativeScoreViewSet, 'api-score')
router.register('vote_scores', VoteScoreViewSet, 'api-votescore')
router.register('votes', RQLVoteViewSet, 'api-vote')
