from django.test import TestCase

from cart.models import Cart, CartLineItem
from liwi import fixtures

class CartModelsTests(TestCase):

    def test_cart_creation_with_user(self):
        """
            test creation of a cart model with a user
        """

        user = fixtures.create_user(
                username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        cart = fixtures.create_cart(user_id=user.id, session_key='1234abc')


        self.assertTrue(isinstance(cart, Cart))

    def test_cart_creation_without_user(self):
        """
            test creation of a cart model without user just sessionkey
        """

        cart = fixtures.create_cart(session_key='1234abc')


        self.assertTrue(isinstance(cart, Cart))