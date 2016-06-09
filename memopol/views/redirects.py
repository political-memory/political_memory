# coding: utf-8

from django.views.generic.base import RedirectView


class RedirectGroupList(RedirectView):
    permanent = True
    query_string = True
    pattern_name = 'group-list'
