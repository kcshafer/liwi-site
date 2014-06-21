from django.test import TestCase

from authentication.forms import LoginForm

class AuthenticationFormsTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_login_form(self):
        """
            test a a valid login form
        """

        post_dict = {'username': 'test_user', 'password': 'password'}
        form = LoginForm(post_dict)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form_no_username(self):
        """
            test a a valid login form
        """

        post_dict = {'username': '', 'password': 'password'}
        form = LoginForm(post_dict)
        self.assertFalse(form.is_valid())

    def test_invalid_login_form_no_password(self):
        """
            test a a valid login form
        """

        post_dict = {'username': 'test_user', 'password': ''}
        form = LoginForm(post_dict)
        self.assertFalse(form.is_valid())