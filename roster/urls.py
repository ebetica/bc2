from django.conf.urls import patterns, url

from roster import views

urlpatterns = patterns('',
    url(r'^$', views.PeopleView.as_view(), name='index'),
    url(r'^people/$', views.PeopleView.as_view(), name='people'),
    url(r'^govboard/$', views.GovboardView.as_view(), name='govboard'),
)