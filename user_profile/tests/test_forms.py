from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import Client

from user_profile.forms import MyProfileForm
from user_profile.models import Profile
from liwi import fixtures

class ProfileFormsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_my_profile_form_valid(self):
        user = fixtures.create_user(
            username='test_user', email="test@user.com", password='password', first_name='Test', last_name='User'
        )
        user_profile = fixtures.create_user_profile(
            user_id=user.id, twitter='', bio='', photo=None
        )
        self.client.login(username=user.username, password='password')
        s = self.client.session
        s['user_id'] = user.id
        s.save()
        upload_file = open('user_profile/tests/resources/test_user.jpg', 'rb')
        post_dict = {'bio': 'Test Bio', 'twitter': 'test_handle'}
        file_dict = {'photo': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = MyProfileForm(post_dict, file_dict)

        profile = Profile.objects.get(id=user_profile.id)

        self.assertTrue(form.is_valid())