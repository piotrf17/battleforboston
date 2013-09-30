from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from mysite import views
from tourny import views as tourny_views

urlpatterns = patterns('',
    # Top level pages, publicly viewable.
    # TODO(piotrf): find a better organization for these.
    url(r'^$', views.index, name='index'),
    url(r'^events$', views.events, name='events'),
    url(r'^directions$', views.directions, name='directions'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^tabata$', views.tabata, name='tabata'),
    url(r'^thanks$', views.thanks, name='thanks'),

    # Tourny app - handles running a tournament.  Registration is also
    # part of this app, but the registration page is publicy viewable,
    # and linked directly off the top level url.
    url(r'^register$', tourny_views.register, name='register'),
    url(r'^tourny/', include('tourny.urls', namespace='tourny')),

    # Admin app.
    url(r'^admin/', include(admin.site.urls)),
)
