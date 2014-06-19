from django.core.files.base import File
from django.test import TestCase

from user_profile.models import Profile
from liwi import fixtures

class UserProfileModelsTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_profile_creation(self):
        """
            Test creation of a profile record
        """
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )
        user_photo = File('art/tests/resources/test_photo.jpg')
        profile = fixtures.create_user_profile(
            user_id=user.id, twitter='test_handle', bio='Test bio', photo=user_photo
        )

        self.assertTrue(isinstance(profile, Profile))