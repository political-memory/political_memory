from django import forms

from datetimewidget.widgets import DateWidget

from .models import Position


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['tags', 'datetime', 'text', 'link', 'representative']
        widgets = {
            # Use localization and bootstrap 3
            'datetime': DateWidget(
                attrs={
                    'id': 'yourdatetimeid'
                },
                usel10n=True,
                bootstrap_version=3,
            ),
            'representative': forms.HiddenInput
        }
