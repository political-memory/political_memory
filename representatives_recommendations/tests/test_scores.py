from django import test
from datetime import datetime
from representatives_votes.models import Proposal, Dossier, Vote
from representatives.models import Representative, Group
from representatives_recommendations.models import Recommendation


class TestScores(test.TestCase):
	def test_group_scores(self):
		prop = Proposal.objects.create(
			dossier	= Dossier.objects.create(
				title = self.id(),
				reference = self.id()
				),
			title = self.id(),
			datetime = datetime.now(),
			total_abstain = 1,
			total_against = 2,
			total_for = 3
			)

		prop.recommendation = Recommendation.objects.create(
			proposal = prop,
			recommendation = "for",
			weight = 10	
			)

		mep0 = Representative.objects.create(
			slug = "mep0",
			full_name = "mep0"
			)


		mep1 = Representative.objects.create(
			slug = "mep1",
			full_name = "mep1"
			)

		
		mep2 = Representative.objects.create(
			slug = "mep2",
			full_name = "mep2"
			)

		group = Group.objects.create(
			name = "group",
			kind = "group"
			)

		mep0.mandates.create(
			group = group,
			link = "http://"
			)

		
		mep1.mandates.create(
			group = group,
			link = "http://"
			)


		mep2.mandates.create(
			group = group,
			link = "http://"
			)

		mep0.votes.create(
			proposal = prop,
			position = "for"
			)


		mep1.votes.create(
			proposal = prop,
			position = "for"
			)

		mep2.votes.create(
			proposal = prop,
			position = "against"
			)

		self.assertEqual(mep0.score.score,10)
		self.assertEqual(mep1.score.score,10)
		self.assertEqual(mep2.score.score,-15)
