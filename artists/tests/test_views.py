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