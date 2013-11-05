# -*- coding:Utf-8 -*-
from django.db import models
from parltrack_meps.models import MEP

class Proposal(models.Model):
    title = models.TextField(null=True)
    code_name =  models.CharField(max_length=255, unique=True)
    date = models.DateField(default=None, null=True, blank=True)


    def __unicode__(self):
        return "%s [%s]" % (self.title if self.title else "no title", self.code_name)

    class Meta:
        ordering = ('-_date', )


class ProposalPart(models.Model):
    datetime = models.DateTimeField()
    subject = models.CharField(max_length=255)
    part = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    proposal = models.ForeignKey(Proposal)

    def __unicode__(self):
        return self.subject

    class MetaClass:
        ordering = ['datetime']


class Vote(models.Model):
    choice = models.CharField(max_length=15, choices=((u'for', u'for'), (u'against', u'against'), (u'abstention', u'abstention'), (u'absent', u'absent')))
    name = models.CharField(max_length=127)
    proposal_part = models.ForeignKey(ProposalPart)
    mep = models.ForeignKey(MEP, null=True)

    class Meta:
        ordering = ["choice"]
        unique_together = ("proposal_part", "mep")

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.choice)
