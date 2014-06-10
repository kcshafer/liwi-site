from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import resolve
from django.test.client import Client
from django.test import TestCase

from authentication import views
from registration.models import User 

class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = Client()

        hashed_password = make_password('password')
        User.objects.create(
                     username='test_user'
                    ,password=hashed_password
                    ,email='test@email.com'
                    ,first_name='test'
                    ,last_name='user'
                    ,is_active=True
                    ,is_superuser=False
                    ,is_staff=False
                    ,is_artist=True 
            )

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

    def test_get_index(self):
        ''' test a get request to the index view '''

        c = Client()
        response = c.get('/login/')
        self.assertTemplateUsed(response, 'authentication/login_form.html')
    
    def test_login_success(self):
        ''' Test a successful login '''

        hashed_password = make_password('password')
        response = self.client.post('/authenticate/', {'username': 'test_user', 'password': 'password'})

        user = User.objects.get(username='test_user')
        self.assertEqual(self.client.session['_auth_user_id'], user.pk)

        response = self.client.get('/art/create/')
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_login_failure(self):
        ''' test a failed login '''

        response = self.client.post('/authenticate/', {'username': 'test_user', 'password': 'pasword'})

        self.assertNotIn('_auth_user_id', self.client.session)

        response = self.client.get('/art/create/')
        self.assertEqual(response.status_code, 302)

    def test_login_no_user(self):
        ''' test a login with a user that doesn not exist '''

        response = self.client.post('/authenticate', {'username': 'fake_user', 'password': 'pass'})
        self.assertNotIn('_auth_user_id', self.client.session)

        response = self.client.get('/art/create/')
        self.assertEqual(response.status_code, 302)

    def test_login_illegal_get(self):
        ''' test that an illegal get call to authenticate is properly trapped '''

        response = self.client.get('/authenticate/')
        self.assertEqual(response.status_code, 405)
