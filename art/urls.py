from django.conf.urls import patterns, url

from art import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create/', views.create_art_form, name='create_art_form'),
    url(r'^upload/', views.upload, name='upload_art')
    )

