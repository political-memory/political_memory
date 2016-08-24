# coding: utf-8

from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView

from representatives.models import Group


class RedirectGroupList(RedirectView):
    permanent = True
    query_string = True
    pattern_name = 'group-list'


class RedirectGroupRepresentativeList(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if kwargs['group_kind'] == 'chamber':
            chamber = Group.objects.get(kind='chamber', name=kwargs['group'])
            return '%s?chamber=%s' % (reverse('representative-list'),
                chamber.pk)
        elif kwargs['group_kind'] == 'country':
            country = Group.objects.get(kind='country', name=kwargs['group'])
            return '%s?country=%s' % (reverse('representative-list'),
                country.pk)
        else:
            group = Group.objects.get(kind=kwargs['group_kind'],
                                      name=kwargs['group'])
            return '%s?group=%s' % (reverse('representative-list'), group.pk)


class RedirectRepresentativeDetail(RedirectView):
    permanent = True
    pattern_name = 'representative-votes'


class RedirectThemeDetail(RedirectView):
    permanent = True
    pattern_name = 'theme-links'


class RedirectDossierDetail(RedirectView):
    permanent = True
    pattern_name = 'dossier-proposals'
