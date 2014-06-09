from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

import home
import authentication

admin.autodiscover()

urlpatterns = patterns('',
    
    #root routes
    url(r'^$', 'home.views.index', name='index'), #home page
    url(r'^authenticate', 'authentication.views.login'),
    url(r'^login', 'authentication.views.index'), #login
    url(r'^logout', 'authentication.views.logout'), #logout
    url(r'^resetpassword/valid', 'authentication.views.validate_answer'), #validate secret question
    url(r'^resetpassword/', 'authentication.views.reset_password'), #validate secret question
    url(r'^forgotpassword', 'authentication.views.forgot_password'), #forgot password

    #complex views
    url(r'^admin/', include(admin.site.urls)), # admin app
    url(r'^registration/', include('registration.urls')), #user registration app
    url(r'^profile/', include('user_profile.urls')), #user profile app
    url(r'^art/', include('art.urls')), # art app
    url(r'^artists/', include('artists.urls')), # artists app

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
