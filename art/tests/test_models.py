from django.core.files.base import File
from django.test import TestCase

from art.models import Art, Like, Category, Tag, ArtTag
from art.tests import fixtures

class ArtModelsTests(TestCase):

    ###### model tests ########

    def test_art_creation(self):
        """
            Test creation of an art record
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        category = fixtures.create_category(name='Test Category')
        art_photo = File('art/tests/resources/test_photo.jpg')
        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo=art_photo, title='Test Art', description='Some art'
        )

        self.assertTrue(isinstance(art, Art))

    def test_category_creation(self):
        """
            Test creation of a category record
        """

        category = fixtures.create_category(name='Test Category')

        self.assertTrue(isinstance(category, Category))

    def test_like_creation(self):
        """
            test creation of an art like record
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        category = fixtures.create_category(name='Test Category')

        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo='test/photo', title='Test Art', description='Some art'
        )

        art_like = fixtures.create_art_like(user_id=user.id, art_id=art.id)

        self.assertTrue(isinstance(art_like, Like))

    def test_tag_creation(self):
        """
            test creation of a tag
        """

        tag = fixtures.create_tag(name='Test Tag')

        self.assertTrue(isinstance(tag, Tag))

    def test_art_tag_creation(self):
        """
            test creation of an art record with tags, and retrieving the tags with the art get_tags
            function
        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        category = fixtures.create_category(name='Test Category')

        art = fixtures.create_art(
            user_id=user.id, category=category.id, photo='test/photo', title='Test Art', description='Some art'
        )

        tag = fixtures.create_tag(name='Test Tag')

        art_tag = fixtures.create_art_tag(art_id=art.id, tag_id=tag.id)

        self.assertTrue(isinstance(art_tag, ArtTag))

        tags = art.get_tags()
        self.assertEqual(tags, 'Test Tag')