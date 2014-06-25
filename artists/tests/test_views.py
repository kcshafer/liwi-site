from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase

from liwi import fixtures

class ArtistViewsTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_artist_index(self):
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        fixtures.create_user_profile(
            user_id=user.id, bio='Test bio', twitter='test_handle', photo=None
        )
        url = reverse("artists.views.index")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_get_featured_authenticated_artist_successful(self):
        """
            test a get request as an authenticated artist to the get_featured view succesfully
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("artists.views.get_featured")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_get_featured_authenticated_artist_existing_fa(self):
        """
            test a get request as an authenticated artist to the get_featured view with an existing fa
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        start = datetime.today()
        end = start + timedelta(days=10)

        fa = fixtures.create_featured_artist(
            user_id=user.id, start_date=start, end_date=end
        )

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("artists.views.get_featured")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    def test_get_featured_authenticated_non_artist(self):
        """
            test a get request as an authenticated non artist to the get_featured view
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user', is_artist=False
        )

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("artists.views.get_featured")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    def test_get_featured_unauthenticated(self):
        """
                test a get request as an unauthenticated user
        """

        url = reverse("artists.views.get_featured")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    def test_post_get_featured_register_successful(self):
        """
            test a post request to the get_featured_register view successully
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        date_format = '%m/%d/%Y'

        start = datetime.today()
        str_start = start.strftime(date_format)
        #TODO: this would fail in december
        end = datetime(start.year, start.month + 1, 1)
        str_end = end.strftime(date_format)

        post_dict = {'start_date': str_start, 'end_date': str_end}
        url = reverse("artists.views.get_featured_register")
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 302)

    def test_post_get_featured_register_no_start_date(self):
        """
            test a post request to the get_featured_register view failing because of no start date
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        date_format = '%m/%d/%Y'

        start = datetime.today()
        str_start = start.strftime(date_format)
        #TODO: this would fail in december
        end = datetime(start.year, start.month + 1, 1)
        str_end = end.strftime(date_format)

        post_dict = {'start_date': '', 'end_date': str_end}
        url = reverse("artists.views.get_featured_register")
        resp = self.client.post(url, post_dict)

        self.assertEqual(resp.status_code, 200)

    def test_get_get_featured_register(self):
        """
            test that get request to the get featured register is blocked
        """
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()

        url = reverse("artists.views.get_featured_register")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 405)
