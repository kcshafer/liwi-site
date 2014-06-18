from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from art.forms import ArtForm
from art.tests import fixtures

class ArtFormsTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_art_form(self):
        category = fixtures.create_category(name='Test Category')
        tag = fixtures.create_tag(name='Test Tag')
        upload_file = open('art/tests/resources/test_photo.jpg', 'rb')
        post_dict = {'title': 'Test Title', 'description': 'Test Description'}
        file_dict = {'photo': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = ArtForm(post_dict, file_dict)
        self.assertTrue(form.is_valid())

    def test_invalid_art_form_no_title(self):
        upload_file = open('art/tests/resources/test_photo.jpg', 'rb')
        post_dict = {'description': 'Test Description'}
        file_dict = {'photo': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = ArtForm(post_dict, file_dict)
        self.assertFalse(form.is_valid())

    def test_invalid_art_form_no_photo(self):
        upload_file = open('art/tests/resources/test_photo.jpg', 'rb')
        post_dict = {'title': 'Test Title', 'description': 'Test Description'}
        file_dict = {'photo': None}
        form = ArtForm(post_dict, file_dict)
        self.assertFalse(form.is_valid())