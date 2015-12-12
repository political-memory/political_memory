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

from representatives.contrib.parltrack.import_representatives import \
    representative_post_save
from representatives.models import Country, Mandate, Representative
from votes.models import MemopolVote


# from django.utils.functional import cached_property


class MemopolRepresentative(Representative):
    country = models.ForeignKey(Country, null=True)
    score = models.IntegerField(default=0)
    main_mandate = models.ForeignKey(Mandate, null=True, default=None)

    def update_score(self):
        score = 0
        for vote in MemopolVote.objects.filter(representative=self):
            score += vote.absolute_score

        self.score = score
        self.save()

    def update_all(self):
        self.update_score()

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


def mempol_representative(sender, representative, data, **kwargs):
    update = False
    try:
        memopol_representative = MemopolRepresentative.objects.get(
            representative_ptr=representative)
    except MemopolRepresentative.DoesNotExist:
        memopol_representative = MemopolRepresentative(
            representative_ptr=representative)

        # Please forgive the horror your are about to witness, but this is
        # really necessary. Django wants to update the parent model when we
        # save a child model.
        memopol_representative.__dict__.update(representative.__dict__)

    try:
        country = sorted(data.get('Constituencies', []),
                         key=lambda c: c.get('end') if c is not None else 1
                         )[-1]['country']
    except IndexError:
        pass
    else:
        if sender.cache.get('countries', None) is None:
            sender.cache['countries'] = {c.name: c.pk for c in
                                         Country.objects.all()}
        country_id = sender.cache['countries'].get(country)

        if memopol_representative.country_id != country_id:
            memopol_representative.country_id = country_id
            update = True

    if sender.mep_cache['groups']:
        main_mandate = sorted(sender.mep_cache['groups'],
                              key=lambda m: m.end_date)[-1]

        if memopol_representative.main_mandate_id != main_mandate.pk:
            memopol_representative.main_mandate_id = main_mandate.pk
            update = True

    if update:
        memopol_representative.save()
representative_post_save.connect(mempol_representative)
