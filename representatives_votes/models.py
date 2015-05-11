# coding: utf-8

from django.db import models


class Dossier(models.Model):
    title = models.CharField(max_length=500)
    reference = models.CharField(max_length=200)
    text = models.TextField()
    link = models.URLField()


class Proposal(models.Model):
    dossier = models.ForeignKey(Dossier)
    title = models.CharField(max_length=500)
    description = models.TextField()
    reference = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    
    total_abstain = models.IntegerField()
    total_against = models.IntegerField()
    total_for = models.IntegerField()


class Vote(models.Model):
    VOTECHOICES = (
        ('abstain', 'abstain'),
        ('for', 'for'),
        ('against', 'against')
    )

    proposal = models.ForeignKey(Proposal)

    representative_slug = models.CharField(max_length=200, blank=True, null=True)
    representative_remote_id = models.CharField(max_length=200, blank=True, null=True)

    position = models.CharField(max_length=10, choices=VOTECHOICES)
