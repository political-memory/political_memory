import models
from django.contrib import admin


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
    list_display = ('representative', 'group', 'role', 'constituency', 'begin_date', 'end_date', 'active')
    search_fields = ('representative', 'group', 'constituency')
    # list_filter = ('role',)


admin.site.register(models.Representative, RepresentativeAdmin)

admin.site.register(models.Country)

admin.site.register(models.Mandate, MandateAdmin)

admin.site.register(models.Group)
admin.site.register(models.Constituency)
