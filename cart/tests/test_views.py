from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from cart.models import Cart
from liwi import fixtures

class CartViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_view_cart_authenticated_new_cart(self):
        """
            test a get request to the view cart view for an auth user
            that has no existing cart
        """
        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )
        self.client.login(username=user.username, password='password')

        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse('cart.views.view_cart')
        resp = self.client.get(url)

        cart = Cart.objects.get()

        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(Cart.objects.get(user_id=user.id))

    def test_view_cart_authenticated_existing_cart(self):
        """
            test a get request to the view cart view for an auth user
            that has an existing cart
        """
        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )

        self.client.login(username=user.username, password='password')

        s = self.client.session
        s['user_id'] = user.id
        s.save()

        cart = fixtures.create_cart(session_key=s._session_key, user_id=user.id)

        url = reverse('cart.views.view_cart')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(Cart.objects.all()), 1)