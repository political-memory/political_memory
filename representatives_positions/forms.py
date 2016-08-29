from django import forms

from datetimewidget.widgets import DateWidget

from memopol_themes.models import Theme
from .models import Position


class PositionForm(forms.ModelForm):
    themes = forms.models.ModelMultipleChoiceField(
        queryset=Theme.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Position
        fields = ['representative', 'link', 'datetime', 'themes', 'text']

        widgets = {
            'datetime': DateWidget(
                usel10n=True,
                bootstrap_version=3
            )
        }

    def save(self, commit=True):
        position = super(PositionForm, self).save(commit=False)

        if commit:
            position.save()

        if position.pk:
            position.themes = self.cleaned_data.get('themes')
            self.save_m2m()

        return position
