from django.conf.urls import patterns, url

from cart import views

urlpatterns = patterns('',
    url(r'view/', views.view_cart, name='view_cart'),
    url(r'^add/([0-9]+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove/([0-9]+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^empty/', views.empty_cart, name='empty_cart'),
    )
