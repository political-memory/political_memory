# coding: utf-8

# This file is part of compotista.
#
# compotista is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# compotista is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2013 Laurent Peuch <cortex@worlddomination.be>
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

from django.contrib import admin

from .models import (Address, Constituency, Country, Email, Group, Mandate,
                     Phone, Representative, WebSite)


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


class MandateInline(admin.StackedInline):
    model = Mandate
    extra = 0


class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'gender', 'birth_place')
    search_fields = ('first_name', 'last_name', 'birth_place')
    list_filter = ('gender', )
    inlines = [
        PhoneInline,
        EmailInline,
        WebsiteInline,
        AdressInline,
        MandateInline
    ]


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation', 'kind')
    list_filter = ('kind',)


class MandateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'representative',
        'group',
        'role',
        'constituency',
        'begin_date',
        'end_date')
    search_fields = ('representative', 'group', 'constituency')


admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(Country)
admin.site.register(Mandate, MandateAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Constituency)
