from django.conf.urls import patterns, url

from registration import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^artlover/', views.artlover_form, name='artlover_form'),
    url(r'^artist/', views.seller_form, name='artist_form'),
    url(r'^activate/([0-9]+)/$', views.activate_user, name='activate_user'),
    )

