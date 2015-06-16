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

from representatives.models import Representative, Group, Country
from representatives_votes.models import Vote

class MemopolRepresentative(Representative):
    
    representative_remote_id = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, null=True)
    score = models.IntegerField(default=0)
    
    def update_score(self):
        score = 0
        for vote in self.representative.votes.all():
            proposal = vote.m_proposal
            if proposal.recommendation:
                recommendation = proposal.recommendation
                if vote.position != recommendation.recommendation:
                    score -= recommendation.weight
                else:
                    score += recommendation.weight
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


    # @property
    # def votes(self):
        # return Vote.objects.filter(
            # representative_remote_id = self.remote_id
        # )

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

class MemopolGroup(Group):
    group = models.OneToOneField(
        Group,
        parent_link = True
    )
    
    active = models.BooleanField(default=False)

    def update_active(self):
        self.active = False
        for mandate in self.mandates.all():
            if mandate.end_date > datetime.date(datetime.now()):
                self.active = True
                break
        self.save()


