from django.conf.urls import patterns, include, url

from memopol_representatives import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^view/(?P<num>\d+)$', views.view, name='view'),
)
