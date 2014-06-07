from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

import home

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'liwi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'home.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registration/', include('registration.urls')),
    url(r'^auth/', include('authentication.urls')),
    url(r'^profile/', include('user_profile.urls')),
    url(r'^art/', include('art.urls')),
    url(r'^artists/', include('artists.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
