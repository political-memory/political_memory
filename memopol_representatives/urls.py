from django.conf.urls import patterns, include, url

from memopol_representatives import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^committee/(?P<committee>\w{4})$', views.committee, name='committee'),
    url(r'^view/(?P<num>\d+)$', views.view, name='view'),
)
