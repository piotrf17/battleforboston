from django.conf.urls import patterns, url

from tourny import views

urlpatterns = patterns('',
  url(r'^competitors$', views.competitor_list, name='competitor_list'),
  url(r'^competitors/(?P<person_id>\d+)$', views.competitor_detail,
      name='competitor_detail'),
  url(r'^competitors/(?P<person_id>\d+)/edit$', views.competitor_edit,
      name='competitor_edit'),
)
