from django.db import models

class Cart(models.Model):

    session_key = models.CharField(max_length=80)
    user = models.ForeignKey('registration.User', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'

class CartLineItem(models.Model):

    art = models.ForeignKey('art.Art')
    cart = models.ForeignKey('cart.Cart')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_line_item'