# coding: utf-8
from django.db import models
from django.db.models.signals import post_save
from django.utils.functional import cached_property

from representatives_votes.contrib.parltrack.import_votes import \
    vote_pre_import
from representatives.contrib.parltrack.import_representatives import \
    representative_pre_import
from representatives_votes.models import Dossier, Proposal, Vote
from representatives.models import Representative


class RepresentativeScore(models.Model):
    representative = models.OneToOneField('representatives.representative',
        primary_key=True, related_name='score')
    score = models.IntegerField(default=0)


class Recommendation(models.Model):
    proposal = models.OneToOneField(
        Proposal,
        related_name='recommendation'
    )

    recommendation = models.CharField(max_length=10, choices=Vote.VOTECHOICES)
    title = models.CharField(max_length=1000, blank=True)
    description = models.TextField(blank=True)
    weight = models.IntegerField(default=0)

    class Meta:
        ordering = ['proposal__datetime']


class ScoredVote(Vote):
    class Meta:
        proxy = True

    @cached_property
    def absolute_score(self):
        recommendation = self.proposal.recommendation

        if self.position == recommendation.recommendation:
            return recommendation.weight
        else:
            return -recommendation.weight


def skip_votes(sender, vote_data=None, **kwargs):
    dossiers = getattr(sender, 'memopol_filters', None)

    if dossiers is None:
        sender.memopol_filters = dossiers = Dossier.objects.filter(
            proposals__recommendation__in=Recommendation.objects.all()
        ).values_list('reference', flat=True)

    if vote_data.get('epref', None) not in dossiers:
        return False
vote_pre_import.connect(skip_votes)


def skip_representatives(sender, representative_data=None, **kwargs):
    if not representative_data.get('active', False):
        return False
representative_pre_import.connect(skip_representatives)


def create_representative_vote_profile(sender, instance=None, created=None,
        **kwargs):

    if not created:
        return

    RepresentativeScore.objects.create(representative=instance)
post_save.connect(create_representative_vote_profile, sender=Representative)


def calculate_representative_score(representative):
    score = 0

    votes = representative.votes.exclude(
        proposal__recommendation=None
    ).select_related('proposal__recommendation')

    votes = ScoredVote.objects.filter(pk__in=votes.values_list('pk'))

    for vote in votes:
        score += vote.absolute_score

    return score
