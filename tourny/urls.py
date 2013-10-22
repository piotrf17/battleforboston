from django.conf.urls import patterns, url

from tourny import views

urlpatterns = patterns('',
  # Competitor management.
  url(r'^competitors$', views.competitor_list, name='competitor_list'),
  url(r'^competitors/(?P<person_id>\d+)$', views.competitor_detail,
      name='competitor_detail'),
  url(r'^competitors/(?P<person_id>\d+)/edit$', views.competitor_edit,
      name='competitor_edit'),
  # Tournament checkin flow.
  url(r'^checkin$', views.checkin, name='checkin'),
  url(r'^accept_payment$', views.accept_payment, name='accept_payment'),
  url(r'^payments$', views.payment_list, name='payment_list'),
  url(r'^payments/(?P<payment_id>\d+)$', views.payment_detail,
      name='payment_detail'),
  # Event management.
  url(r'^events$', views.event_list, name='event_list'),
  url(r'^events/gen_default$', views.generate_default_events,
      name='generate_default_events'),
  url(r'^events/(?P<event_id>\d+)$', views.event_detail, name='event_detail')
)
