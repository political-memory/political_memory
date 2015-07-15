from __future__ import absolute_import

from django.contrib import admin

from representatives.models import Email, WebSite, Address, Phone, Country
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



# class MandateAdmin(admin.ModelAdmin):
    # list_display = ('representative', 'group', 'role', 'constituency', 'begin_date', 'end_date', 'active')
    # search_fields = ('representative', 'group', 'constituency')
    # list_filter = ('role',)


# admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(MemopolRepresentative, MemopolRepresentativeAdmin)
# admin.site.register(Country)

# admin.site.register(MemopolMandate, MandateAdmin)

# admin.site.register(MemopolGroup)
# admin.site.register(Constituency)
