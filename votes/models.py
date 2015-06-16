# coding: utf-8

# This file is part of memopol.
#
# memopol is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# memopol is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

from django.db import models

from representatives_votes.models import Vote, Proposal, Dossier
from legislature.models import MemopolRepresentative

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


class MemopolDossier(Dossier):
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True)

class MemopolVote(Vote):
    class Meta:
        proxy = True

    @property
    def representative(self):
        return MemopolRepresentative.objects.get(
            remote_id = self.representative_remote_id
        )
