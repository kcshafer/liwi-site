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

    ###### TODO ####################
    ##### Django doesn't allow me (or I haven't figured out how) too set the session key for #######
    ##### an unauth user to test that cart is saved and created for unauth users ###################

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

    def test_add_to_cart_authenticated_new_cart(self):
        """
            test an item being added to the cart via post request
        """
        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )

        artist_user = fixtures.create_user(
            username='test_user2', email="test@user.com", password='password', first_name='Test', last_name='User'
        )
        self.client.login(username=user.username, password='password')

        s = self.client.session
        s['user_id'] = user.id
        s.save()

        art = fixtures.create_art(user_id=artist_user.id, category='test', photo='/whatever/', title='test art', description='test art')

        url = reverse('cart.views.add_to_cart', args=(art.id, ))
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 200)

    def test_add_to_cart_authenticated_existing_cart(self):
        """
            test an item being added to the cart via post request existing cart
        """
        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )

        artist_user = fixtures.create_user(
            username='test_user2', email="test@user.com", password='password', first_name='Test', last_name='User'
        )
        self.client.login(username=user.username, password='password')

        s = self.client.session
        s['user_id'] = user.id
        s.save()

        cart = fixtures.create_cart(session_key=s._session_key, user_id=user.id)

        art = fixtures.create_art(user_id=artist_user.id, category='test', photo='/whatever/', title='test art', description='test art')

        url = reverse('cart.views.add_to_cart', args=(art.id, ))
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 200)

    def test_remove_from_cart(self):
        """
            test removing an item from cart successfully
        """

        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )

        artist_user = fixtures.create_user(
            username='test_user2', email="test@user.com", password='password', first_name='Test', last_name='User'
        )
        self.client.login(username=user.username, password='password')

        s = self.client.session
        s['user_id'] = user.id
        s.save()

        cart = fixtures.create_cart(session_key=s._session_key, user_id=user.id)

        art = fixtures.create_art(user_id=artist_user.id, category='test', photo='/whatever/', title='test art', description='test art')

        cli = fixtures.create_cart_line_item(cart_id=cart.id, art_id=art.id)

        url = reverse('cart.views.remove_from_cart', args=(cli.id, ))
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 200)

    def test_empty_cart(self):
        """
            test empty =cart successfully
        """

        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )

        artist_user = fixtures.create_user(
            username='test_user2', email="test@user.com", password='password', first_name='Test', last_name='User'
        )
        self.client.login(username=user.username, password='password')

        s = self.client.session
        s['user_id'] = user.id
        s.save()

        cart = fixtures.create_cart(session_key=s._session_key, user_id=user.id)

        art = fixtures.create_art(user_id=artist_user.id, category='test', photo='/whatever/', title='test art', description='test art')

        cli = fixtures.create_cart_line_item(cart_id=cart.id, art_id=art.id)

        url = reverse('cart.views.empty_cart')
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 200)




