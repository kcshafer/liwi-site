from django.core.urlresolvers import resolve
from django.test.client import Client
from django.test import TestCase

from authentication import views

class AuthenticationTests(TestCase):

    #############################
    #### TEST ALL URL ROUTES ####
    #############################

    def test_index_route(self):
        ''' Test that the the authentication index maps to the view.index '''

        index_url = resolve('/login/')
        self.assertEqual(index_url.func, views.index)

    def test_login_route(self):
        ''' Test that /login/ maps to views.login '''

        login_url = resolve('/authenticate/')
        self.assertEqual(login_url.func, views.login)

    def test_logout_route(self):
        ''' Test that /logout/ maps to views.logout '''

        logout_url = resolve('/logout/')
        self.assertEqual(logout_url.func, views.logout)

    def test_forgot_password_route(self):
        ''' test that /forgotpassword/ maps to views.forgot_password '''

        forgot_password_url = resolve('/forgotpassword/')
        self.assertEqual(forgot_password_url.func, views.forgot_password)

    def test_validate_answer_route(self):
        ''' Test that /resetpassword/valid routes to views.validate_answer '''

        reset_password_valid_url = resolve('/resetpassword/valid/')
        self.assertEqual(reset_password_valid_url.func, views.validate_answer)

    def test_reset_password_route(self):
        ''' Test that /resetpassword/ reoutes to views.reset_password '''

        reset_password_url = resolve('/resetpassword/')
        self.assertEqual(reset_password_url.func, views.reset_password)               
