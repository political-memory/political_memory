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

from representatives.models import Address, Country, Email, Phone, WebSite

from .models import MemopolRepresentative


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0


class WebsiteInline(admin.TabularInline):
    model = WebSite
    extra = 0


class AdressInline(admin.StackedInline):
    model = Address
    extra = 0


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0


class CountryInline(admin.TabularInline):
    model = Country
    extra = 0


class MemopolRepresentativeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'country', 'score', 'main_mandate')
    search_fields = ('first_name', 'last_name', 'birth_place')
    list_filter = ('gender', 'active')
    inlines = [
        PhoneInline,
        EmailInline,
        WebsiteInline,
        AdressInline,
    ]


admin.site.register(MemopolRepresentative, MemopolRepresentativeAdmin)
