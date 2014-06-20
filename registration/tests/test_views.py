import os
from urlparse import urlparse

from django.contrib.messages import constants as MSG
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from liwi import fixtures

class RegistrationViewsTests(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        os.system('rm -rf test_photos/user/*')


    def test_index(self):
        """
            test the registration index
        """

        url = reverse('registration.views.index')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_artlover_form_get(self):
        """
            test a get request to the artlover form
        """

        url = reverse(('registration.views.artlover_form'))
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_artlover_form_post(self):
        """
            test a post request to the art lover form
        """
        post_dict = {
            'password': 'password', 'username': 'test_user',
            'email': 'test@email.com', 'first_name': 'test',
            'last_name': 'user'
        }

        url = reverse(('registration.views.artlover_form'))
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 302)

    def test_seller_form_get(self):
        """
            test a get request to the seller form
        """

        url = reverse('registration.views.seller_form')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_seller_form_post(self):
        """
            test a post request to the seller form
        """

        post_dict = {
            'password': 'password', 'username': 'test_user',
            'email': 'test@email.com', 'first_name': 'test',
            'last_name': 'user'
        }

        url = reverse('registration.views.seller_form')
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 302)

    def test_activate_user_success(self):
        """
            test a post request to the user activate view, with a user id that has not been activated
        """

        user = fixtures.create_user(
            username='test_user', password='password',
            email='user@test.com', first_name='test',
            last_name='user', is_active=False
        )

        url = reverse('registration.views.activate_user', args=[user.id])
        resp = self.client.post(url, follow=True)
        messages = list(resp.context['messages'])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(messages), 0)

    def test_activate_user_failure(self):
        """
            test a post request to the user activate view, with a user id that has been activated
        """

        user = fixtures.create_user(
            username='test_user', password='password',
            email='user@test.com', first_name='test',
            last_name='user', is_active=True
        )

        url = reverse('registration.views.activate_user', args=[user.id])
        resp = self.client.post(url, follow=True)
        messages = list(resp.context['messages'])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, MSG.ERROR)

    def test_view_account_authenticated(self):
        """
            test that an authenticated request to view the user account is successful
        """
        user = fixtures.create_user(
            username='test_user', password='password',
            email='user@test.com', first_name='test',
            last_name='user'
        )

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse('registration.views.view_account')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_view_account_unauthenticated(self):
        """
            test an unauthenticated request to view an account
        """

        url = reverse('registration.views.view_account')
        resp = self.client.get(url, follow=True)
        resp_url = (resp.__dict__.get('redirect_chain')[0])[0]
        parsed_url = urlparse(resp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(parsed_url.path, '/login')
        self.assertEqual(parsed_url.query, 'next=/account/')

    def test_edit_account_authenticated(self):
        """
            test that an authenticated request to edit the user account is successful
        """
        user = fixtures.create_user(
            username='test_user', password='password',
            email='user@test.com', first_name='test',
            last_name='user'
        )

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse('registration.views.edit_account')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_edit_account_unauthenticated(self):
        """
            test that an unauthenticated request to edit the user account is not successful
        """
        user = fixtures.create_user(
            username='test_user', password='password',
            email='user@test.com', first_name='test',
            last_name='user'
        )

        url = reverse('registration.views.edit_account')
        resp = self.client.get(url, follow=True)
        resp_url = (resp.__dict__.get('redirect_chain')[0])[0]
        parsed_url = urlparse(resp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(parsed_url.path, '/login')
        self.assertEqual(parsed_url.query, 'next=/account/edit/')

    def test_save_account_post(self):
        """
            test that a post request to the save account view is successful
        """

        user = fixtures.create_user(
            username='test_user', password='password',
            email='user@test.com', first_name='test',
            last_name='user'
        )

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        post_dict = {'city': 'new york', 'state': 'new york', 'twitter': 'test_handle'}
        url = reverse('registration.views.save_account')
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 302)

    def test_save_account_get(self):
        """
            test that a get request to the save account view is not successful
        """

        user = fixtures.create_user(
            username='test_user', password='password',
            email='user@test.com', first_name='test',
            last_name='user'
        )

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse('registration.views.save_account')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 405)
        self.assertEqual(resp.__dict__.get('reason_phrase'), 'METHOD NOT ALLOWED')

    def test_save_account_unauthenticated(self):
        """
            test that a unauthenticated post request to the save account view is not successful
        """

        user = fixtures.create_user(
            username='test_user', password='password',
            email='user@test.com', first_name='test',
            last_name='user'
        )

        post_dict = {'twitter': 'test_handle'}

        url = reverse('registration.views.save_account')
        resp = self.client.post(url, follow=True)
        resp_url = (resp.__dict__.get('redirect_chain')[0])[0]
        parsed_url = urlparse(resp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(parsed_url.path, '/login')
        self.assertEqual(parsed_url.query, 'next=/account/save/')
