from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView


class TabRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if 'tab' in kwargs:
            tab = kwargs.pop('tab')
            return reverse('%s-%s' % (self.pattern_base, tab), args=args,
                           kwargs=kwargs)
        else:
            return reverse('%s-detail' % self.pattern_base, args=args,
                           kwargs=kwargs)


class RepresentativeListRedirect(RedirectView):
    permanent = True
    query_string = True
    pattern_name = 'representative-list'


class RepresentativeDetailRedirect(TabRedirectView):
    pattern_base = 'representative'


class DossierListRedirect(RedirectView):
    permanent = True
    query_string = True
    pattern_name = 'dossier-list'


class DossierDetailRedirect(TabRedirectView):
    pattern_base = 'dossier'


class ThemeListRedirect(RedirectView):
    permanent = True
    query_string = True
    pattern_name = 'theme-list'


class ThemeDetailRedirect(RedirectView):
    permanent = True
    pattern_name = 'theme-detail'


urlpatterns = [
    # Representative list

    url(
        r'^legislature/representative/$',
        RepresentativeListRedirect.as_view(),
        name='legacy-representative-list'
    ),

    # Representative detail

    url(
        r'^legislature/representative/(?P<slug>[-\w]+)/$',
        RepresentativeDetailRedirect.as_view(),
        name='legacy-representative-detail'
    ),

    url(
        r'^legislature/representative/(?P<slug>[-\w]+)/(?P<tab>\w+)/$',
        RepresentativeDetailRedirect.as_view(),
        name='legacy-representative-detail'
    ),

    # Dossier list

    url(
        r'^votes/dossier/$',
        DossierListRedirect.as_view(),
        name='legacy-dossier-list'
    ),

    # Dossier detail

    url(
        r'^votes/dossier/(?P<pk>\d+)/$',
        DossierDetailRedirect.as_view(),
        name='legacy-dossier-detail'
    ),

    url(
        r'^votes/dossier/(?P<pk>\d+)/(?P<tab>\w+)/$',
        DossierDetailRedirect.as_view(),
        name='legacy-dossier-detail'
    ),

    # Theme list

    url(
        r'^theme/$',
        ThemeListRedirect.as_view(),
        name='legacy-theme-list'
    ),

    # Theme detail

    url(
        r'^theme/(?P<slug>[-\w]+)/$',
        ThemeDetailRedirect.as_view(),
        name='legacy-theme-detail'
    ),
]
