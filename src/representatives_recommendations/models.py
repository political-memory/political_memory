# coding: utf-8
from django.db import models

from representatives_votes.contrib.parltrack.import_votes import \
    vote_pre_import
from representatives_votes.models import Dossier, Proposal, Vote


class Recommendation(models.Model):
    proposal = models.OneToOneField(
        Proposal,
        related_name='recommendation'
    )

    recommendation = models.CharField(max_length=10, choices=Vote.VOTECHOICES)
    title = models.CharField(max_length=1000, blank=True)
    description = models.TextField(blank=True)
    weight = models.FloatField(default=0)

    class Meta:
        ordering = ['proposal__datetime']


def skip_votes(sender, vote_data=None, **kwargs):
    dossiers = getattr(sender, 'memopol_filters', None)

    if dossiers is None:
        sender.memopol_filters = dossiers = Dossier.objects.filter(
            proposals__recommendation__in=Recommendation.objects.all()
        ).values_list('reference', flat=True)

    if vote_data.get('epref', None) not in dossiers:
        return False
vote_pre_import.connect(skip_votes)
