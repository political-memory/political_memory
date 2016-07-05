# coding: utf-8

from django.contrib import admin

from .models import Dossier, Proposal, Vote


class DossierAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'title', 'link')
    search_fields = ('reference', 'title')


class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'dossier_reference',
        'title',
        'kind')
    search_fields = ('reference', 'dossier__reference', 'title')

    def dossier_reference(self, obj):
        return obj.dossier.reference


class NoneMatchingFilter(admin.SimpleListFilter):
    title = 'Representative'
    parameter_name = 'representative'

    def lookups(self, request, model_admin):
        return [('None', 'Unknown')]

    def queryset(self, request, queryset):
        if self.value() == 'None':
            return queryset.filter(representative=None)
        else:
            return queryset


class VoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'proposal_reference',
        'position',
        'representative',
        'representative_name')
    list_filter = (NoneMatchingFilter,)

    def proposal_reference(self, obj):
        return obj.proposal.reference

admin.site.register(Dossier, DossierAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Vote, VoteAdmin)
