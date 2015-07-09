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

from datetime import datetime

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property

from representatives.models import Representative, Mandate, Country
from representatives_votes.models import Vote
from core.utils import create_child_instance_from_parent


class MemopolRepresentative(Representative):
    country = models.ForeignKey(Country, null=True)
    score = models.IntegerField(default=0)
    
    def update_score(self):
        score = 0
        for vote in self.votes.all():
            proposal = vote.proposal
            try:
                if proposal.recommendation:
                    recommendation = proposal.recommendation
                    if ( vote.position != recommendation.recommendation
                         and (
                             vote.position == 'abstain' or
                             recommendation.recommendation == 'abstain' )):
                        score -= (recommendation.weight / 2)
                    elif vote.position != recommendation.recommendation:
                        score -= recommendation.weight
                    else:
                        score += recommendation.weight
            except Exception:
                pass

        self.score = score
        self.save()

    def update_country(self):
        # Create a country if it does'nt exist
        # The representative's country is the one associated
        # with the last 'country' mandate
        try:
            country_mandate = self.mandates.filter(
                group__kind='country'
            ).order_by('-begin_date')[0:1].get()

            country, _ = Country.objects.get_or_create(
                name=country_mandate.group.name,
                code=country_mandate.group.abbreviation
            )
            self.country = country
            self.save()

        except ObjectDoesNotExist:
            self.country = None
            self.save()

    def active_mandates(self):
        return self.mandates.filter(
            end_date__gte=datetime.now()
        )

    def former_mandates(self):
        return self.mandates.filter(
            end_date__lte=datetime.now()
        )
    
    def current_group_mandate(self):
        return self.mandates.get(
            end_date__gte=datetime.now(),
            group__kind='group'
        )

@receiver(post_save, sender=Representative)
def create_memopolrepresentative_from_representative(instance, **kwargs):
    memopol_representative = create_child_instance_from_parent(MemopolRepresentative, instance)
    memopol_representative.update_country()
    memopol_representative.save()

@receiver(post_save, sender=Mandate)
def update_memopolrepresentative_country(instance, created, **kwargs):
    return
    if not created:
        return

    # Update representative country
    if instance.group.kind == 'country' and instance.representative.extra.country == None:
        instance.representative.extra.update_country()

