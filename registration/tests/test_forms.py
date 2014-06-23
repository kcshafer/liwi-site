from django.test import TestCase

from liwi import fixtures
from registration.forms import CustomerRegistration, SellerRegistration, AccountForm

class RegistrationFormsTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_buyer_registration_form(self):
        """
            test a valid buyer registration form
        """

        post_dict = {
            'password': 'password', 'username': 'test_user',
            'email': 'test@email.com', 'first_name': 'test',
            'last_name': 'user'
        }

        form = CustomerRegistration(post_dict)
        self.assertTrue(form.is_valid())

    def test_invalid_buyer_registration_form_dupe_username(self):
        """
            test an invalid buyer registration form caused by a duplicate username
        """

        user = fixtures.create_user(
            username='test_user', password='password',
            email='user2@test.com', first_name='test',
            last_name='user'
        )

        post_dict = {
            'password': 'password', 'username': 'test_user',
            'email': 'test@email.com', 'first_name': 'test',
            'last_name': 'user'
        }

        form = CustomerRegistration(post_dict)

        self.assertFalse(form.is_valid())
        self.assertIn('User with this Username already exists.', form.errors['username'])

    def test_invalid_buyer_registration_form_dupe_email(self):
        """
            test an invalid buyer registration form caused by a duplicate email
        """

        user = fixtures.create_user(
            username='test_user', password='password',
            email='test@test.com', first_name='test',
            last_name='user'
        )

        post_dict = {
            'password': 'password', 'username': 'test_user2',
            'email': 'test@test.com', 'first_name': 'test',
            'last_name': 'user'
        }

        form = CustomerRegistration(post_dict)

        self.assertFalse(form.is_valid())
        self.assertIn('This email is already registered.', form.errors['email'])