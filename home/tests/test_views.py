from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from liwi import fixtures

class HomeViewsTests(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_index_get(self):
        """
            test a get request to the index view
        """

        url = reverse('home.views.index')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_contact_form_authenticated_successful(self):
        """
            test a get request to the contact view by an authenticated user
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse('home.views.contact')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_contact_form_unauthenticated_successful(self):
        """
            test a get request to the contact view by an unauthenticated user
        """

        url = reverse('home.views.contact')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_contact_send_post_authenticated_successful(self):
        """
            test a post request to the contact send view by an authenticated user
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        post_dict = {'subject': 'test_subject', 'body': 'test body', 'email': 'test@email.com'}
        url = reverse('home.views.contact_send')
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 302)

    def test_contact_send_post_unauthenticated_successful(self):
        """
            test a post request to the contact send view by an unauthenticated user
        """

        post_dict = {'subject': 'test_subject', 'body': 'test body', 'email': 'test@email.com'}
        url = reverse('home.views.contact_send')
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 302)

    def test_contact_send_post_unauthenticated_failure_email(self):
        """
            test a post request to the contact send view by an unauthenticated user
        """

        post_dict = {'subject': 'test_subject', 'body': 'test body', 'email': ''}
        url = reverse('home.views.contact_send')
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 302)

    def test_contact_send_post_unauthenticated_failure_subject(self):
        """
            test a post request to the contact send view by an unauthenticated user failing on subject
        """

        post_dict = {'subject': '', 'body': 'test body', 'email': 'test@email.com'}
        url = reverse('home.views.contact_send')
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 302)

    def test_contact_send_post_unauthenticated_failure_body(self):
        """
            test a post request to the contact send view by an unauthenticated user failing on body
        """

        post_dict = {'subject': 'test subhect', 'body': '', 'email': 'test@email.com'}
        url = reverse('home.views.contact_send')
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 302)

    def test_contact_send_get(self):
        """
            test a get request to the contact send is blocked
        """

        post_dict = {'subject': 'test_subject', 'body': 'test body', 'email': 'test@email.com'}
        url = reverse('home.views.contact_send')
        resp = self.client.get(url, post_dict)

        self.assertEqual(resp.status_code, 405)