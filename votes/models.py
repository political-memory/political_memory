# coding: utf-8
from django.db import models
from django.utils.functional import cached_property
from django.db.models.signals import post_save
from django.dispatch import receiver

from representatives_votes.management.commands import (
        parltrack_import_votes,)
# from representatives.models import Representative
from representatives_votes.models import Vote, Proposal, Dossier
# from legislature.models import MemopolRepresentative
from core.utils import create_child_instance_from_parent


class Recommendation(models.Model):
    SCORE_TABLE = {
        ('abstain', 'abstain'): 1,
        ('abstain', 'for'): -0.5,
        ('abstain', 'against'): -0.5,
    }

    VOTECHOICES = (
        ('abstain', 'abstain'),
        ('for', 'for'),
        ('against', 'against')
    )

    proposal = models.OneToOneField(
        Proposal,
        related_name='recommendation'
    )

    recommendation = models.CharField(max_length=10, choices=VOTECHOICES)
    title = models.CharField(max_length=1000, blank=True)
    description = models.TextField(blank=True)
    weight = models.IntegerField(default=0)

    class Meta:
        ordering = ['proposal__datetime']


class MemopolDossier(Dossier):
    dossier_reference = models.CharField(max_length=200)
    name = models.CharField(max_length=1000, blank=True, default='')
    description = models.TextField(blank=True, default='')

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.dossier_ptr.title
        return super(MemopolDossier, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

@receiver(post_save, sender=Dossier)
def create_memopolrepresentative_from_representative(instance, **kwargs):
    create_child_instance_from_parent(MemopolDossier, instance)


class MemopolVote(Vote):
    class Meta:
        proxy = True

    @cached_property
    def absolute_score(self):
        if not self.proposal.recommendation_id:
            return 0

        recommendation = self.proposal.recommendation

        weight = recommendation.weight
        if (self.position == 'abstain' or
                recommendation.recommendation == 'abstain'):
            weight = weight / 2
        if self.position == recommendation.recommendation:
            return weight
        else:
            return -weight


def vote_pre_import(sender, vote_data=None, **kwargs):
    dossiers = getattr(sender, 'memopol_filters', None)

    if dossiers is None:
        sender.memopol_filters = dossiers = Dossier.objects.filter(
            proposals__recommendation__in=
                Recommendation.objects.all()
        ).values_list('reference', flat=True)

    if vote_data.get('epref', None) not in dossiers:
        return False
parltrack_import_votes.Command.vote_pre_import.connect(vote_pre_import)
