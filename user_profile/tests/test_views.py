import os

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from liwi import fixtures

class UserProfileViewsTests(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        os.system('rm -rf test_photos/art/*')
        os.system('rm -rf test_photos/user/*')

    def test_view_profile(self):
        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )
        #HACK: create the art directory for the user that matches what we insert into the db
        os.system('mkdir test_photos/user/%s' % user.id)
        os.system('cp user_profile/tests/resources/test_user.jpg test_photos/user/%s/' % user.id)
        os.system('mkdir test_photos/art/%s' % user.id)
        os.system('cp art/tests/resources/test_photo.jpg test_photos/art/%s/' % user.id)

        user_profile = fixtures.create_user_profile(
            user_id=user.id, twitter='test_handle', bio='test_bio', photo=('test_photos/user/%s/test_user.jpg' % user.id)
        )

        category = fixtures.create_category(name='Test Category')

        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )

        url = reverse("user_profile.views.view_profile", args=(user.id, ))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_edit_profile(self):
        """
            Test the edit profile view
        """

        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )
        #HACK: create the art directory for the user that matches what we insert into the db
        os.system('mkdir test_photos/user/%s' % user.id)
        os.system('cp user_profile/tests/resources/test_user.jpg test_photos/user/%s/' % user.id)
        os.system('mkdir test_photos/art/%s' % user.id)
        os.system('cp art/tests/resources/test_photo.jpg test_photos/art/%s/' % user.id)

        user_profile = fixtures.create_user_profile(
            user_id=user.id, twitter='test_handle', bio='test_bio', photo=('test_photos/user/%s/test_user.jpg' % user.id)
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("user_profile.views.edit_profile")

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_save_profile_post(self):
        """
            test the save profile view with a post
            returns 302 as a redirect to the profile view
        """
        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )
        #HACK: create the art directory for the user that matches what we insert into the db
        os.system('mkdir test_photos/user/%s' % user.id)
        os.system('cp user_profile/tests/resources/test_user.jpg test_photos/user/%s/' % user.id)
        os.system('mkdir test_photos/art/%s' % user.id)
        os.system('cp art/tests/resources/test_photo.jpg test_photos/art/%s/' % user.id)

        user_profile = fixtures.create_user_profile(
            user_id=user.id, twitter='test_handle', bio='test_bio', photo=('test_photos/user/%s/test_user.jpg' % user.id)
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("user_profile.views.save_profile")

        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 302)

    def test_save_profile_get(self):
        """
            test the save profile view with a post
            returns 405 for get not allowed
        """
        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )
        #HACK: create the art directory for the user that matches what we insert into the db
        os.system('mkdir test_photos/user/%s' % user.id)
        os.system('cp user_profile/tests/resources/test_user.jpg test_photos/user/%s/' % user.id)
        os.system('mkdir test_photos/art/%s' % user.id)
        os.system('cp art/tests/resources/test_photo.jpg test_photos/art/%s/' % user.id)

        user_profile = fixtures.create_user_profile(
            user_id=user.id, twitter='test_handle', bio='test_bio', photo=('test_photos/user/%s/test_user.jpg' % user.id)
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("user_profile.views.save_profile")

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 405)