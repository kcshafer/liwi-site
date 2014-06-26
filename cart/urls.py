from django.conf.urls import patterns, url

from cart import views

urlpatterns = patterns('',
    url(r'view/', views.view_cart, name='view_cart'),
    url(r'^add/([0-9]+)/$', views.add_to_cart, name='add_to_cart'),
    )
