from dal import autocomplete

from django import forms

from models import Recommendation


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = '__all__'
        widgets = {
            'proposal': autocomplete.ModelSelect2(
                url='proposal-autocomplete',
            )
        }
