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

from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView

from .forms import PositionForm
from .models import Position


class PositionCreate(CreateView):
    """Create a position"""
    model = Position
    fields = PositionForm.Meta.fields + ['representative']

    def get_success_url(self):
        return reverse('legislature:representative-detail',
                       kwargs={'name': self.object.representative.slug})


class PositionDetail(DetailView):
    """Display a position"""
    model = Position
    queryset = Position.objects.filter(published=True)
