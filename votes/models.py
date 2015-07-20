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
from django.utils.functional import cached_property
from django.db.models.signals import post_save
from django.dispatch import receiver

from representatives.models import Representative
from representatives_votes.models import Vote, Proposal, Dossier
from legislature.models import MemopolRepresentative
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
