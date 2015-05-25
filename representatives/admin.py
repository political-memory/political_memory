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
    # list_filter = ('role',)


admin.site.register(Representative, RepresentativeAdmin)

admin.site.register(Country)

admin.site.register(Mandate, MandateAdmin)

admin.site.register(Group)
admin.site.register(Constituency)
