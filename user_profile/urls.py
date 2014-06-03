from django.conf.urls import patterns, url

from user_profile import views

urlpatterns = patterns('',
    url(r'^myprofile/edit', views.edit_profile, name='edit_profile'),
    url(r'^view/([0-9])/$', views.view_profile, name='view_profile'),
    )

