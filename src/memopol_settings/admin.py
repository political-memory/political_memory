from django.contrib import admin

from .models import Setting


class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'comment')
    list_editable = ('key', 'value', 'comment')
    list_filter = ('key',)

admin.site.register(Setting, SettingAdmin)
