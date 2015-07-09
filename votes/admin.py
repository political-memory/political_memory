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
from django.core.urlresolvers import reverse

from .admin_views import import_vote_with_recommendation, import_vote, update_representatives_score
from .models import Recommendation, MemopolDossier


admin.site.register_view('import_vote', view=import_vote)
admin.site.register_view('import_vote_with_recommendation', view=import_vote_with_recommendation)
admin.site.register_view('update_representatives_score', view=update_representatives_score)

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

    list_display = ('id', 'title', link_to_proposal, 'recommendation','weight')
    search_fields = ('title', 'recommendation', 'proposal')

admin.site.register(MemopolDossier, MemopolDossierAdmin)
admin.site.register(Recommendation, RecommendationsAdmin)
