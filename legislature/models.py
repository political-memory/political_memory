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
# from django.utils.functional import cached_property

from representatives.models import Representative, Mandate, Country
from votes.models import MemopolVote
from core.utils import create_child_instance_from_parent


class MemopolRepresentative(Representative):
    country = models.ForeignKey(Country, null=True)
    score = models.IntegerField(default=0)
    main_mandate = models.ForeignKey(Mandate, null=True, default=None)

    def update_score(self):
        score = 0
        for vote in self.votes.all():
            score += vote.absolute_score

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
        except ObjectDoesNotExist:
            self.country = None
        self.save()

    def update_main_mandate(self):
        try:
            self.main_mandate = self.mandates.get(
                end_date__gte=datetime.now(),
                group__kind='group'
            )
        except Mandate.DoesNotExist:
            self.main_mandate = None
        self.save()

    def update_all(self):
        self.update_country()
        self.update_score()
        self.update_main_mandate()

    def active_mandates(self):
        return self.mandates.filter(
            end_date__gte=datetime.now()
        )

    def former_mandates(self):
        return self.mandates.filter(
            end_date__lte=datetime.now()
        )

    def votes_with_proposal(self):
        return MemopolVote.objects.select_related(
            'proposal',
            'proposal__recommendation'
        ).filter(representative=self)


@receiver(post_save, sender=Representative)
def create_memopolrepresentative_from_representative(instance, **kwargs):
    memopol_representative = create_child_instance_from_parent(MemopolRepresentative, instance)
    memopol_representative.save()
