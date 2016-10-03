# coding: utf-8

from django.views import generic

from memopol_themes.models import Theme

from representatives_positions.views import PositionFormMixin


class ThemeDetailBase(PositionFormMixin, generic.DetailView):
    template_name = 'memopol_themes/theme_detail.html'

    queryset = Theme.objects.all()

    def get_context_data(self, **kwargs):
        c = super(ThemeDetailBase, self).get_context_data(**kwargs)
        c['position_form'].fields['themes'].initial = [c['object']]

        return c
