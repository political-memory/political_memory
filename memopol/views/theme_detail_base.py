# coding: utf-8

from django.views import generic

from memopol_themes.models import Theme


class ThemeDetailBase(generic.DetailView):
    template_name = 'memopol_themes/theme_detail.html'

    queryset = Theme.objects.all()
