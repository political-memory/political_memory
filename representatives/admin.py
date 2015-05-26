# This file is part of django-representatives.
#
# django-representatives is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# django-representatives is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with Foobar.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2013 Laurent Peuch <cortex@worlddomination.be>
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

# coding: utf-8

from django.contrib import admin
from .models import Representative, Country, Mandate, Group, Constituency, Email, WebSite, Phone, Address


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
    list_display = ('full_name', 'gender', 'birth_place')
    search_fields = ('first_name', 'last_name', 'birth_place')
    list_filter = ('gender', )
    inlines = [
        PhoneInline,
        EmailInline,
        WebsiteInline,
        AdressInline,
        MandateInline
    ]


class MandateAdmin(admin.ModelAdmin):
    list_display = ('representative', 'group', 'role', 'constituency', 'begin_date', 'end_date')
    search_fields = ('representative', 'group', 'constituency')


admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(Country)
admin.site.register(Mandate, MandateAdmin)
admin.site.register(Group)
admin.site.register(Constituency)
