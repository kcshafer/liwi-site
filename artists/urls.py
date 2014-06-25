from django.conf.urls import patterns, url

from artists import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'getfeatured/register/', views.get_featured_register, name='get_featured_register'),
    url(r'getfeatured/', views.get_featured, name='index'),
    )

pass