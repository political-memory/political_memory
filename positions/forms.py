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

from datetimewidget.widgets import DateWidget
from django import forms

from .models import Position


class PositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = ['tags', 'datetime', 'text', 'link']
        widgets = {
            # Use localization and bootstrap 3
            'datetime': DateWidget(
                attrs={
                    'id': 'yourdatetimeid'
                },
                usel10n=True,
                bootstrap_version=3,
            )
        }
