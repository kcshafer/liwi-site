from datetime import datetime

from django.test import TestCase
from django.test.client import Client

from artists.forms import FeaturedArtistForm
from liwi import fixtures

class ArtistFormsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_featured_artist_form_valid(self):
        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
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

        form = FeaturedArtistForm(post_dict)

        self.assertTrue(form.is_valid())

    def test_featured_artist_form_invalid_date_greater(self):
        """
            test the featured artist form fails with a greater start date than end date
        """

        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
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

        post_dict = {'start_date': str_end, 'end_date': str_start}

        form = FeaturedArtistForm(post_dict)

        self.assertFalse(form.is_valid())