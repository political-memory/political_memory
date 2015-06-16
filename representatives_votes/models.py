# coding: utf-8

# This file is part of toutatis.
#
# toutatis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# toutatis is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.

from django.db import models


class Dossier(models.Model):
    title = models.CharField(max_length=1000)
    reference = models.CharField(max_length=200)
    text = models.TextField(blank=True, default='')
    link = models.URLField()


class Proposal(models.Model):
    dossier = models.ForeignKey(Dossier, related_name='proposals')
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True, default='')
    reference = models.CharField(max_length=200, blank=True, null=True)
    datetime = models.DateTimeField()
    kind = models.CharField(max_length=200, blank=True, default='')
    total_abstain = models.IntegerField()
    total_against = models.IntegerField()
    total_for = models.IntegerField()

    # Presentation for the api
    def vote_api_list(self):
        return [{'position': vote.position,
                 'representative_remote_id': vote.representative_remote_id,
                 'representative_name': vote.representative_name
             }
            for vote in self.vote_set.all()]


class Vote(models.Model):
    VOTECHOICES = (
        ('abstain', 'abstain'),
        ('for', 'for'),
        ('against', 'against')
    )

    proposal = models.ForeignKey(Proposal, related_name='votes')

    # There are two representative fields for flexibility,
    representative_name = models.CharField(max_length=200, blank=True, null=True)
    representative_remote_id = models.CharField(max_length=200, blank=True, null=True)

    position = models.CharField(max_length=10, choices=VOTECHOICES)
