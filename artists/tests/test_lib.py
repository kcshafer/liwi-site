from datetime import datetime

from django.test import TestCase

from artists.lib.featured_artist import retrieve_featured_artists
from artists.models import FeaturedArtist
from liwi import fixtures

class FeaturedArtistLibTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_retrieve_featured_artists(self):

        date_format = '%m/%d/%Y'

        start = datetime.today()
        str_start = start.strftime(date_format)
        #TODO: this would fail in december
        end = datetime(start.year, start.month + 1, 1)
        str_end = end.strftime(date_format)

        for i in range(1, 10):
            user = fixtures.create_user(
                username='test_user' + str(i), password='password', email='user' + str(i) + '@test.com', first_name='test', last_name='user'
            )

            fa = fixtures.create_featured_artist(
                user_id=user.id, start_date=start, end_date=end, photo='\whatever'
            )

        featured_artists = retrieve_featured_artists(5)
        first_fa_ids = []
        for fa in featured_artists:
            first_fa_ids.append(fa.id)

        self.assertEqual(len(featured_artists), 5)
        self.assertEqual(featured_artists[0].total_imprints, 1)

        next_featured_artists = retrieve_featured_artists(5)
        next_fa_ids = []

        for fa in next_featured_artists:
            next_fa_ids.append(fa.id)

        self.assertNotEqual(first_fa_ids, next_fa_ids)
