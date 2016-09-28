# coding: utf-8
from django.db import models

from representatives.models import Chamber, Representative, TimeStampedModel


class Dossier(TimeStampedModel):
    title = models.CharField(max_length=1000)
    reference = models.CharField(max_length=200, unique=True)
    text = models.TextField(blank=True, default='')

    class Meta:
        unique_together = (('title', 'reference'))

    def __unicode__(self):
        return unicode(self.title)

    def chambers(self):
        """
        Return distinct chambers. You probably want to prefetch
        documents__chamber before calling that.
        """

        # Use sorted() because using order_by will hit the database no matter
        # what was prefetched
        return set(sorted([d.chamber for d in self.documents.all()]))


class Document(TimeStampedModel):
    dossier = models.ForeignKey(Dossier, related_name='documents')
    chamber = models.ForeignKey(Chamber)
    title = models.CharField(max_length=1000)
    kind = models.CharField(max_length=255, blank=True, default='')
    link = models.URLField(max_length=1000)


class Proposal(TimeStampedModel):
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

    class Meta:
        ordering = ['datetime']
        unique_together = (('dossier', 'title', 'reference',
                            'kind', 'total_abstain', 'total_against',
                            'total_for'))

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
