from django.conf.urls import patterns, url

from vroom import views

urlpatterns = patterns('',
    url(r'([0-9]+)/', views.index, name='index'),
    url(r'^upload/', views.upload, name='upload_room'),
)
