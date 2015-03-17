from django.conf.urls import patterns, include, url

from memopol_representatives import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^committee/(?P<mandate_abbr>\w{4})$',
        views.by_mandate, {'mandate_kind': 'committee'}, name='committee'),
    url(r'^listby/(?P<mandate_kind>\w+)/a/(?P<mandate_abbr>.+)$',
        views.by_mandate, name='listby'),
    url(r'^listby/(?P<mandate_kind>\w+)/n/(?P<mandate_name>.+)$',
        views.by_mandate, name='listby'),
    url(r'^view/(?P<num>\d+)$', views.view, name='view'),
)
