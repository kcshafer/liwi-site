from urlparse import urlparse

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from liwi import fixtures

class AuthenticationViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_index_unauthenticated(self):
        """
            test an authenticated get request to the authentication index
        """

        url = reverse('authentication.views.index')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200

    )

    def test_login_post_successful(self):
        """
            test a post login request from a existing user to the login view
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        post_dict = {'username': 'test_user', 'password': 'password'}

        url = reverse('authentication.views.login')
        resp = self.client.post(url, post_dict, follow=True)

        self.assertEqual(resp.status_code, 200)

    def test_login_post_successful_redirect(self):
        """
            test a post login request from a existing user to the login view, with a next parameter for redirect
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        post_dict = {'username': 'test_user', 'password': 'password', 'next': '/art/'}

        url = reverse('authentication.views.login')
        resp = self.client.post(url, post_dict, follow=True)
        resp_url = (resp.__dict__.get('redirect_chain')[0])[0]
        parsed_url = urlparse(resp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(parsed_url.path, '/art/')

    def test_login_post_wrong_password(self):
        """
            test a post login request with the correct username but incorrect password
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        post_dict = {'username': 'test_user', 'password': 'wrong_password', 'next': '/art/'}

        url = reverse('authentication.views.login')
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.__dict__.get('_container')[0], 'User not found or password incorrect')

    def test_login_post_no_user(self):
        """
            test a post login request with a username that does not exist
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        post_dict = {'username': 'fake_user', 'password': 'password'}

        url = reverse('authentication.views.login')
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.__dict__.get('_container')[0], 'User not found or password incorrect')

    def test_login_get(self):
        """
            test that a get request to the login view is properly blocked
        """

        url = reverse('authentication.views.login')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 405)
        self.assertEqual(resp.__dict__.get('reason_phrase'), 'METHOD NOT ALLOWED')


    def test_logout(self):
        """
            test a request to the logout view
        """

        url = reverse('authentication.views.logout')
        resp = self.client.get(url, follow=True)
        resp_url = (resp.__dict__.get('redirect_chain')[0])[0]
        parsed_url = urlparse(resp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(parsed_url.path, '/login/')

    def test_forgot_password_post_user_exists(self):
        """
            test a post request to the forgot password view for an existing user
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        post_dict = {'username': 'test_user'}

        url = reverse('authentication.views.forgot_password')
        resp = self.client.post(url, post_dict, follow=True)
        resp_url = (resp.__dict__.get('redirect_chain')[0])[0]
        parsed_url = urlparse(resp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(parsed_url.path, '/resetpassword/valid/')

    def test_forgot_password_post_no_user(self):
        """
            test a post request to the forgot password view for an non existing user
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        post_dict = {'username': 'fake_user'}

        url = reverse('authentication.views.forgot_password')
        resp = self.client.post(url, post_dict, follow=True)
        resp_url = (resp.__dict__.get('redirect_chain')[0])[0]
        parsed_url = urlparse(resp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(parsed_url.path, '/forgotpassword/')

    def test_forgot_password_get(self):
        """
            test a get request to the forgot password view
        """

        url = reverse('authentication.views.forgot_password')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_validate_answer_post_correct(self):
        """
            test a post request to the validate answer view with a correct answer
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        cache.set('user_id', user.id, 30)
        post_dict = {'secret_answer': 'Test Answer'}

        url = reverse('authentication.views.validate_answer')
        resp = self.client.post(url, post_dict, follow=True)

        self.assertEqual(resp.status_code, 200)

    def test_validate_answer_post_incorrect(self):
        """
            test a post request to the validate answer view with a incorrect answer
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        cache.set('user_id', user.id, 30)
        post_dict = {'secret_answer': 'Test Wrong Answer'}

        url = reverse('authentication.views.validate_answer')
        resp = self.client.post(url, post_dict, follow=True)

        self.assertEqual(resp.status_code, 200)

    def test_validate_answer_post_timeout(self):
        """
            test a post request to the validate answer view where the cached user id times out
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        cache.set('user_id', user.id, 0.0000001)
        post_dict = {'secret_answer': 'Test Answer'}

        url = reverse('authentication.views.validate_answer')
        resp = self.client.post(url, post_dict, follow=True)
        resp_url = (resp.__dict__.get('redirect_chain')[0])[0]
        parsed_url = urlparse(resp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(parsed_url.path, '/resetpassword/forgotpassword/')

    def test_validate_answer_get(self):
        """
            test a get request to the validate answer view
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        cache.set('user_id', user.id, 30)
        post_dict = {'secret_answer': 'Test Answer'}

        url = reverse('authentication.views.validate_answer')
        resp = self.client.get(url, follow=True)

        self.assertEqual(resp.status_code, 200)

    def test_validate_answer_get_timeout(self):
        """
            test a get request to the validate answer view where the cache times out
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        cache.set('user_id', user.id, 0.0000001)

        url = reverse('authentication.views.validate_answer')
        resp = self.client.get(url, follow=True)
        resp_url = (resp.__dict__.get('redirect_chain')[0])[0]
        parsed_url = urlparse(resp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(parsed_url.path, '/resetpassword/forgotpassword/')

    def test_reset_password_get(self):
        """
            test a get request to the reset password view
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        cache.set('user_id', user.id, 30)

        url = reverse('authentication.views.reset_password')
        resp = self.client.get(url, follow=True)

        self.assertEqual(resp.status_code, 200)

    def test_reset_password_post_success(self):
        """
            test a post request to the reset password view successfully
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        cache.set('user_id', user.id, 30)
        post_dict = {'password': 'new_password', 're_password': 'new_password'}

        url = reverse('authentication.views.reset_password')
        resp = self.client.post(url, post_dict, follow=True)
        resp_url = (resp.__dict__.get('redirect_chain')[0])[0]
        parsed_url = urlparse(resp_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(parsed_url.path, '/login/')

    def test_reset_password_post_match_failure(self):
        """
            test a post request to the reset password view failing password match
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        cache.set('user_id', user.id, 30)
        post_dict = {'password': 'new_password', 're_password': 'new_password2'}

        url = reverse('authentication.views.reset_password')
        resp = self.client.post(url, post_dict, follow=True)

        self.assertEqual(resp.status_code, 200)

    def test_reset_password_post_timeout(self):
        """
            test a post request to the reset password view failing bc of timeout
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        secret_question = fixtures.create_security_question(question='Test')

        fixtures.create_secret_answer(
            user_id=user.id, question_id=secret_question.id, answer='Test Answer'
        )

        cache.set('user_id', user.id, 0.000001)
        post_dict = {'password': 'new_password', 're_password': 'new_password2'}

        url = reverse('authentication.views.reset_password')
        resp = self.client.post(url, post_dict, follow=True)

        self.assertEqual(resp.status_code, 200)

