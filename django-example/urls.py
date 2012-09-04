### -*- coding: utf-8 -*- ###

from django.conf import settings
from django.conf.urls.defaults import include, url, patterns
from django.contrib import admin

from views import home

admin.autodiscover()

urlpatterns = patterns('views',
    url(r'^$', 'home', name='home'),
    url(r'^show_notes/$', 'show_notes', name='show_notes'),
    url(r'^admin/', include(admin.site.urls))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
    )