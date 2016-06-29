# coding: utf-8
from django.db import models

from representatives_votes.contrib.parltrack.import_votes import \
    vote_pre_import
from representatives_votes.models import Dossier, Proposal, Vote
from representatives.models import Representative


class DossierScore(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    representative = models.ForeignKey(Representative,
        on_delete=models.DO_NOTHING)
    dossier = models.ForeignKey(Dossier, on_delete=models.DO_NOTHING)
    score = models.FloatField(default=0)

    class Meta:
        managed = False
        db_table = 'representatives_recommendations_dossierscores'


class VoteScore(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='votescores')

    representative = models.ForeignKey(
        Representative, related_name='votescores', null=True)
    position = models.CharField(max_length=10)
    score = models.FloatField(default=0)

    class Meta:
        managed = False
        ordering = ['proposal__datetime']
        db_table = 'representatives_recommendations_votescores'


class RepresentativeScore(models.Model):
    representative = models.OneToOneField('representatives.representative',
        primary_key=True, related_name='score')
    score = models.FloatField(default=0)

    class Meta:
        managed = False
        db_table = 'representatives_recommendations_representativescore'


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
