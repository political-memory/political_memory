# coding: utf-8

from django.db import models


class Dossier(models.Model):
    title = models.CharField(max_length=1000)
    reference = models.CharField(max_length=200)
    text = models.TextField()
    link = models.URLField()


class Proposal(models.Model):
    dossier = models.ForeignKey(Dossier)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    reference = models.CharField(max_length=200, null=True)
    datetime = models.DateTimeField()
    kind = models.CharField(max_length=200, null=True)
    total_abstain = models.IntegerField()
    total_against = models.IntegerField()
    total_for = models.IntegerField()

    # Presentation for the api
    def vote_api_list(self):
        return [
            {'position': vote.position,
             'representative': vote.representative_remote_id}
            for vote in self.vote_set.all()]
        

class Vote(models.Model):
    VOTECHOICES = (
        ('abstain', 'abstain'),
        ('for', 'for'),
        ('against', 'against')
    )

    proposal = models.ForeignKey(Proposal)

    # There are two representative fields for flexibility,
    representative_name = models.CharField(max_length=200, blank=True, null=True)
    representative_remote_id = models.CharField(max_length=200, blank=True, null=True)

    position = models.CharField(max_length=10, choices=VOTECHOICES)
