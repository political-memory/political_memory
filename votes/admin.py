# coding: utf-8
from __future__ import absolute_import

from autocomplete_light import shortcuts as ac
from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Recommendation, MemopolDossier

def link_to_edit(obj, field):
    try:
        related_obj = getattr(obj, field)
        url = reverse(
            'admin:{}_{}_change'.format(
                related_obj._meta.app_label,
            related_obj._meta.object_name.lower()
            ),
            args=(related_obj.pk,)

        )
        return '&nbsp;<strong><a href="{url}">{obj}</a></strong>'.format(url=url,obj=related_obj)

    except:
        return '???'

class MemopolDossierAdmin(admin.ModelAdmin):

    list_display = ('name', 'dossier_ptr')
    search_fields = ('name',)

    fields = ('dossier_ptr', 'name')
    readonly_fields = ('dossier_ptr',)


class RecommendationsAdmin(admin.ModelAdmin):
    def link_to_proposal(self):
        return link_to_edit(self, 'proposal')
    link_to_proposal.allow_tags = True

    list_display = ('id', 'title', 'proposal', 'recommendation','weight')
    search_fields = ('title', 'recommendation', 'proposal')
    form = ac.modelform_factory(Recommendation, exclude=[])

admin.site.register(MemopolDossier, MemopolDossierAdmin)
admin.site.register(Recommendation, RecommendationsAdmin)
