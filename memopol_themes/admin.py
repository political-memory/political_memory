from django import forms
from django.contrib import admin

from representatives_votes.admin import DossierAdmin, ProposalAdmin
from representatives_votes.models import Dossier, Proposal

from representatives_positions.admin import PositionAdmin
from representatives_positions.models import Position

from .models import Theme, ThemeLink


class LinkInline(admin.StackedInline):
    model = ThemeLink
    extra = 0


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_editable = ('name', 'description')
    list_filter = ('name',)
    fields = ('name', 'description')
    inlines = [
        LinkInline
    ]


class ThemeLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime', 'link')
    list_editable = ('title', 'datetime', 'link')
    list_filter = ('title', 'datetime', 'link')


class ThemedAdminForm(forms.ModelForm):
    themes = forms.ModelMultipleChoiceField(
        queryset=Theme.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple(
            verbose_name='Themes',
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super(ThemedAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['themes'].initial = self.instance.themes.all()

    def save(self, commit=True):
        item = super(ThemedAdminForm, self).save(commit=False)

        if commit:
            item.save()

        if item.pk:
            item.themes = self.cleaned_data['themes']
            self.save_m2m()

            return item


class ThemedDossierAdminForm(ThemedAdminForm):
    class Meta:
        model = Dossier
        fields = ('title', 'reference', 'text', 'themes')


class ThemedProposalAdminForm(ThemedAdminForm):
    class Meta:
        model = Proposal
        fields = ('dossier', 'title', 'description', 'reference', 'datetime',
                  'kind', 'total_abstain', 'total_against', 'total_for',
                  'themes')


class ThemedPositionAdminForm(ThemedAdminForm):
    class Meta:
        model = Position
        fields = ('representative', 'datetime', 'text', 'link', 'published',
                  'themes')


class ThemedDossierAdmin(DossierAdmin):
    form = ThemedDossierAdminForm


class ThemedProposalAdmin(ProposalAdmin):
    form = ThemedProposalAdminForm


class ThemedPositionAdmin(PositionAdmin):
    form = ThemedPositionAdminForm


admin.site.register(Theme, ThemeAdmin)
admin.site.register(ThemeLink, ThemeLinkAdmin)

admin.site.unregister(Dossier)
admin.site.register(Dossier, ThemedDossierAdmin)

admin.site.unregister(Proposal)
admin.site.register(Proposal, ThemedProposalAdmin)

admin.site.unregister(Position)
admin.site.register(Position, ThemedPositionAdmin)
