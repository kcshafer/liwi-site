from django.core.urlresolvers import resolve
from django.test.client import Client 
from django.test import TestCase

from registration.forms import CustomerRegistration
from registration.models import User
from registration.views import index, artlover_form, seller_form, activate_user

class RegistrationTest(TestCase):

    #############################
    #### TEST ALL URL ROUTES ####
    #############################

    def test_index_route(self):
        ''' Test that the registration index maps to the view.index function '''

        index_url = resolve('/registration/')
        self.assertEqual(index_url.func, index)

    def test_artlover_route(self):
        ''' Test that  /registration/artlover/ maps to views.artlover_form '''

        artlover_url = resolve('/registration/artlover/')
        self.assertEqual(artlover_url.func, artlover_form)

    def test_artist_route(self):
        ''' test that /registration/artist/ maps to views.seller_form ''' 

        artist_url = resolve('/registration/artist/')
        self.assertEqual(artist_url.func, seller_form)

    def test_activate_route(self):
        ''' test that /registration/activate/1/ maps to views.activate_user '''

        activate_url = resolve('/registration/activate/1/')
        self.assertEqual(activate_url.func, activate_user)


    #### TEST REQUESTS TO ROUTES ####
    def test_get_index(self):
        ''' test that the registration index renders the correct template '''

        c = Client()
        response = c.get('/registration/')
        
        self.assertTemplateUsed(response, 'registration/index.html')

    def test_get_artlover_form(self):
        ''' test a get request to the artlover_form view '''

        c = Client()
        response = c.get('/registration/artlover/')

        self.assertTemplateUsed(response, 'registration/buyer_form.html')

    def test_post_artlover_form(self):
        ''' test a post request to the art_lover form view '''

        c = Client()
        response = c.post('/registration/artlover/', {'username': 'buyer_test', 'email': 'test_email@test.com', 'password': 'test_password', 'first_name': 'test', 'last_name': 'user'})
        new_user = User.objects.get(username='buyer_test')

        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, 'test_email@test.com')
        self.assertFalse(new_user.is_active)
        self.assertFalse(new_user.is_staff)
        self.assertFalse(new_user.is_artist)
        self.assertFalse(new_user.is_superuser)
    
    def test_get_artist_form(self):
        ''' test a get request to the artlover_form view '''

        c = Client()
        response = c.get('/registration/artist/')

        self.assertTemplateUsed(response, 'registration/register.html')

    def test_post_artist_form(self):
        ''' test a post request to the artist form view '''

        c = Client()
        response = c.post('/registration/artist/', {'username': 'seller_test', 'email': 'test_artist@test.com', 'password': 'test_password', 'first_name': 'test', 'last_name': 'user'})
        new_user = User.objects.get(username='seller_test')

        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, 'test_artist@test.com')
        self.assertFalse(new_user.is_active)
        self.assertFalse(new_user.is_staff)
        self.assertFalse(new_user.is_superuser)

    def test_activate_artist(self):
        ''' test a post request to the activate user view for an artist user '''

        c = Client()
        response = c.post('/registration/artist/', {'username': 'artist_activate_test', 'email': 'activate_artist@test.com', 'password': 'test_password', 'first_name': 'test', 'last_name': 'user'})
        new_user = User.objects.get(username='artist_activate_test')

        self.assertFalse(new_user.is_active)

        response = c.post(('/registration/activate/%s/' %  new_user.id))

        active_user = User.objects.get(username='artist_activate_test')

        self.assertTrue(active_user.is_active)
        self.assertRedirects(response, '/login/')

