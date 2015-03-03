from django.contrib import admin

import representatives.models as models
from memopol_representatives.models import MemopolRepresentative


class EmailInline(admin.TabularInline):
    model = models.Email
    extra = 0


class WebsiteInline(admin.TabularInline):
    model = models.WebSite
    extra = 0


class AdressInline(admin.StackedInline):
    model = models.Address
    extra = 0


class PhoneInline(admin.TabularInline):
    model = models.Phone
    extra = 0


class MandateInline(admin.StackedInline):
    model = models.Mandate
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
    list_display = ('kind', 'name', 'constituency', 'representative')
    search_fields = ('kind', 'name')
    list_filter = ('kind',)

admin.site.register(MemopolRepresentative, RepresentativeAdmin)

admin.site.register(models.Country)
admin.site.register(models.Mandate, MandateAdmin)
