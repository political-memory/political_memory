# coding: utf-8
from __future__ import absolute_import

from django.contrib import admin

from .forms import RecommendationForm
from .models import Recommendation


class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'proposal', 'recommendation', 'weight')
    search_fields = ('title', 'description', 'proposal__title',
                     'proposal__dossier__title')
    form = RecommendationForm

admin.site.register(Recommendation, RecommendationsAdmin)
