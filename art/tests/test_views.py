import os

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from liwi import fixtures

class ArtViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        os.system('rm -rf test_photos/art/*')
        os.system('rm -rf test_photos/user/*')

    def test_art_index_unauthenticated(self):
        url = reverse("art.views.index")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_my_art_admin_artist_authenticated(self):
        """
            test a get request to the my artist admin view as an authenticated artist
        """
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        category = fixtures.create_category(name='Test Category')
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )
        like = fixtures.create_art_like(user_id=user.id, art_id=art.id)
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("art.views.my_art_admin")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_my_art_admin_artist_unauthenticated(self):
        """
            test a get request to the my artist admin view as an unauthenticated artist
        """
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        category = fixtures.create_category(name='Test Category')
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )
        like = fixtures.create_art_like(user_id=user.id, art_id=art.id)

        url = reverse("art.views.my_art_admin")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    def test_my_art_admin_non_artist_authenticated(self):
        """
            test a get request to the my artist admin view as an authenticated non artist
        """
        art_user = fixtures.create_user(
            username='test_artist', password='password', email='art@test.com', first_name='art', last_name='user'
        )

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user', is_artist=False
        )
        category = fixtures.create_category(name='Test Category')
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % art_user.id), title='Test Art', description='Some art'
        )
        like = fixtures.create_art_like(user_id=user.id, art_id=art.id)

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("art.views.my_art_admin")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)


    def test_art_index_authenticated(self):
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        category = fixtures.create_category(name='Test Category')
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )
        like = fixtures.create_art_like(user_id=user.id, art_id=art.id)
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()
        url = reverse("art.views.index")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_create_art_form_artist(self):
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()
        url = reverse("art.views.create_art_form")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_create_art_form_non_artist(self):
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user', is_artist=False
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()
        url = reverse("art.views.create_art_form")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_upload_post(self):
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()
        url = reverse("art.views.upload")
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 200)

    def test_upload_get(self):
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()
        url = reverse("art.views.upload")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 405)

    def test_view_art_unauthenticated(self):
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        category = fixtures.create_category(name='Test Category')
        os.system('mkdir test_photos/art/%s' % user.id)
        os.system('cp art/tests/resources/test_photo.jpg test_photos/art/%s/' % user.id)
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )
        url = reverse("art.views.view_art_single", args=(art.id, ))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_view_art_authenticated(self):
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()
        category = fixtures.create_category(name='Test Category')
        os.system('mkdir test_photos/art/%s' % user.id)
        os.system('cp art/tests/resources/test_photo.jpg test_photos/art/%s/' % user.id)
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )
        url = reverse("art.views.view_art_single", args=(art.id, ))

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_like_art(self):
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()
        category = fixtures.create_category(name='Test Category')

        #HACK: create the art directory for the user that matches what we insert into the db
        os.system('mkdir test_photos/art/%s' % user.id)
        os.system('cp art/tests/resources/test_photo.jpg test_photos/art/%s/' % user.id)

        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )
        url = reverse("art.views.like_art", args=(art.id, ))

        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 200)

    def test_handle_art_activation_authenticated_post_artist(self):
        """
            test a post request to the handle_art_activation authenticated with an artist user
        """
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        category = fixtures.create_category(name='Test Category')
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )
        like = fixtures.create_art_like(user_id=user.id, art_id=art.id)
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("art.views.handle_art_activation", args=(art.id, ))
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.__dict__.get('_container')[0], 'Activate')

    def test_handle_art_deactivation_authenticated_post_artist(self):
        """
            test a post request to the handle_art_activation deactivation authenticated with an artist user
        """
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        category = fixtures.create_category(name='Test Category')
        art = fixtures.create_art(
            user_id=user.id, category=category.id,
            photo=('test_photos/art/%s/test_photo.jpg' % user.id), active=False,
            title='Test Art', description='Some art'
        )
        like = fixtures.create_art_like(user_id=user.id, art_id=art.id)
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("art.views.handle_art_activation", args=(art.id, ))
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.__dict__.get('_container')[0], 'Deactivate')

    def test_handle_art_activation_authenticated_post_artist(self):
        """
            test a post request to the handle_art_activation authenticated with an artist user
        """
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        category = fixtures.create_category(name='Test Category')
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )
        like = fixtures.create_art_like(user_id=user.id, art_id=art.id)
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("art.views.handle_art_activation", args=(art.id, ))
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.__dict__.get('_container')[0], 'Activate')

    def test_handle_art_activation_unauthenticated_post_(self):
        """
            test a post request to the handle_art_activation unauthenticated
        """
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        category = fixtures.create_category(name='Test Category')
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )
        like = fixtures.create_art_like(user_id=user.id, art_id=art.id)

        url = reverse("art.views.handle_art_activation", args=(art.id, ))
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)

    def test_handle_art_action_get(self):
        """
            test a get request to the handle_art_activation
        """
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        category = fixtures.create_category(name='Test Category')
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=('test_photos/art/%s/test_photo.jpg' % user.id), title='Test Art', description='Some art'
        )
        like = fixtures.create_art_like(user_id=user.id, art_id=art.id)
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("art.views.handle_art_activation", args=(art.id, ))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 405)