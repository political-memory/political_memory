# coding: utf-8
from django.db import models

from representatives.models import (HashableModel, Representative,
                                    TimeStampedModel)


class Dossier(HashableModel, TimeStampedModel):
    title = models.CharField(max_length=1000)
    reference = models.CharField(max_length=200, unique=True)
    text = models.TextField(blank=True, default='')
    link = models.URLField()
    ext_link = models.URLField(blank=True, default='')

    hashable_fields = ['title', 'reference']

    def __unicode__(self):
        return unicode(self.title)


class Proposal(HashableModel, TimeStampedModel):
    dossier = models.ForeignKey(Dossier, related_name='proposals')
    title = models.CharField(max_length=1000, unique=True)
    description = models.TextField(blank=True, default='')
    reference = models.CharField(max_length=200, blank=True, null=True)
    datetime = models.DateTimeField(db_index=True)
    kind = models.CharField(max_length=200, blank=True, default='')
    total_abstain = models.IntegerField()
    total_against = models.IntegerField()
    total_for = models.IntegerField()

    representatives = models.ManyToManyField(
        Representative, through='Vote', related_name='proposals'
    )

    hashable_fields = ['dossier', 'title', 'reference',
                       'kind', 'total_abstain', 'total_against',
                       'total_for']

    class Meta:
        ordering = ['datetime']

    @property
    def status(self):
        if self.total_for > self.total_against:
            return 'adopted'
        else:
            return 'rejected'

    def __unicode__(self):
        return unicode(self.title)


class Vote(models.Model):
    VOTECHOICES = (
        ('abstain', 'abstain'),
        ('for', 'for'),
        ('against', 'against')
    )

    proposal = models.ForeignKey(Proposal, related_name='votes')

    representative = models.ForeignKey(
        Representative, related_name='votes', null=True)
    # Save representative name in case of we don't find the representative
    representative_name = models.CharField(max_length=200, blank=True)

    position = models.CharField(max_length=10, choices=VOTECHOICES)

    class Meta:
        ordering = ['proposal__datetime']
        unique_together = (('proposal', 'representative'))
