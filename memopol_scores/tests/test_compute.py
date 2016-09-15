from datetime import date, timedelta

from django import test

from memopol_scores.models import RepresentativeScore
from memopol_settings.models import Setting
from representatives.models import Representative
from representatives_positions.models import Position
from representatives_recommendations.models import Recommendation
from representatives_votes.models import Dossier, Proposal


class ComputeTest(test.TestCase):
    fixtures = ['compute_score.json']

    @property
    def representative(self):
        return Representative.objects.get(last_name='TEST')

    @property
    def dossier(self):
        return Dossier.objects.get(reference='TEST')

    @property
    def good_proposal(self):
        return Proposal.objects.get(dossier=self.dossier, reference='GOOD')

    @property
    def bad_proposal(self):
        return Proposal.objects.get(dossier=self.dossier, reference='BAD')

    def refresh(self):
        RepresentativeScore.refresh()

    def set_decay(self, days, exponent, decimals=0):
        params = {
            "SCORE_DECAY_NUM": 1,
            "SCORE_DECAY_DENOM": days,
            "SCORE_EXPONENT": exponent,
            "SCORE_DECIMALS": decimals
        }

        for k, v in params.iteritems():
            setting = Setting.objects.get(key=k)
            setting.value = '%s' % v
            setting.save()

    def set_good_recommendation(self, weight):
        rec = Recommendation(
            proposal=self.good_proposal,
            recommendation='for',
            title='Good',
            description='Good',
            weight=weight
        )
        rec.save()
        return rec

    def set_bad_recommendation(self, weight):
        rec = Recommendation(
            proposal=self.bad_proposal,
            recommendation='against',
            title='Bad',
            description='Bad',
            weight=weight
        )
        rec.save()
        return rec

    def create_position(self, when, score):
        pos = Position(
            representative=self.representative,
            datetime=when,
            kind='other',
            title='TEST',
            text='TEST',
            link='http://www.example.com',
            score=score,
            published=True
        )
        pos.save()
        return pos

    def test_no_score(self):
        self.refresh()

        assert self.representative.representative_score.score == 0

    def test_good_vote_score(self):
        self.set_good_recommendation(100)
        self.refresh()

        assert self.representative.representative_score.score == 100

    def test_bad_vote_score(self):
        self.set_bad_recommendation(100)
        self.refresh()

        assert self.representative.representative_score.score == -100

    def test_decay(self):
        proposal = self.good_proposal
        proposal.datetime = date.today() - timedelta(365)
        proposal.save()

        self.set_good_recommendation(100)
        self.set_decay(365, 1)
        self.refresh()

        assert self.representative.representative_score.score == 37

    def test_position(self):
        self.create_position(date.today(), 100)
        self.refresh()

        assert self.representative.representative_score.score == 100

    def test_total(self):
        self.set_good_recommendation(100)
        self.set_bad_recommendation(10)
        self.create_position(date.today(), 1)
        self.refresh()

        assert self.representative.representative_score.score == 100 - 10 + 1
