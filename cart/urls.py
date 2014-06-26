from django.conf.urls import patterns, url

from cart import views

urlpatterns = patterns('',
    url(r'view/', views.view_cart, name='view+cart'),
    )
