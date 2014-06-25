from datetime import datetime
from datetime import timedelta

from django.test import TestCase

from artists.models import FeaturedArtist
from liwi import fixtures

class ArtistModelsTests(TestCase):

    def test_featured_artist_creation(self):
        """
            test creation of an artist model record
        """

        user = fixtures.create_user(
                username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        start = datetime.today()
        end = start + timedelta(days=10)

        fa = fixtures.create_featured_artist(
            user_id=user.id, start_date=start, end_date=end, photo='\whatever'
        )


        self.assertTrue(isinstance(fa, FeaturedArtist))