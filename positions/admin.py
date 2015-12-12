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
from __future__ import absolute_import

from django.contrib import admin

from .models import Position


def publish_positions(modeladmin, request, queryset):
    """Set published to True for the queryset"""
    queryset.update(published=True)

publish_positions.short_description = 'Publish selected positions'


def unpublish_positions(modeladmin, request, queryset):
    """Set published to False for the queryset"""
    queryset.update(published=False)

unpublish_positions.short_description = 'Unpublish selected positions'


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'representative',
        'short_text',
        'datetime',
        'link',
        'published')
    list_display_links = ('short_text',)
    list_editable = ('published',)
    list_filter = ('published',)
    actions = (publish_positions, unpublish_positions)

admin.site.register(Position, PositionAdmin)
