from django.conf import settings
from django.conf.urls import url

import views

urlpatterns = [
    url(
        r'^dossier/(?P<pk>\d+)/$',
        views.DossierDetail.as_view(),
        name='dossier-detail'
    ),
    url(
        r'dossier/$',
        views.DossierList.as_view(),
        name='dossier-list'
    ),
]

if 'dal_select2' in settings.INSTALLED_APPS:
    from autocompletes import ProposalAutocomplete  # noqa

    urlpatterns.append(
        url(
            'autocomplete/proposal/$',
            ProposalAutocomplete.as_view(),
            name='proposal-autocomplete',
        ),
    )
