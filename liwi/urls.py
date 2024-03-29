from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

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
    url(r'^account/edit/', 'registration.views.edit_account', name='edit_settings'),
    url(r'^account/save/', 'registration.views.save_account', name='save_account'),
    url(r'^account/changepassword/', 'registration.views.change_password', name='change_password'),
    url(r'^account/', 'registration.views.view_account', name='view_settings'),
    url(r'^myart/', 'art.views.my_art_admin', name='my_art_admin'),
    url(r'contact/send/', 'home.views.contact_send', name='contact send'),
    url(r'contact/', 'home.views.contact', name='contact us'),

    #complex views
    url(r'^admin/', include(admin.site.urls)), # admin app
    url(r'^registration/', include('registration.urls')), #user registration app
    url(r'^profile/', include('user_profile.urls')), #user profile app
    url(r'^art/', include('art.urls')), # art app
    url(r'^artists/', include('artists.urls')), # artists app
    url(r'^cart/', include('cart.urls')), #shopping cart app

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
